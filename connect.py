import os
import sys
import time
import logging
import datetime
import threading
import urllib.request
import urllib.error
import configparser
from threading import Thread, current_thread
from threading import *
from monga_client.client.ks_client import KeystoneClient
from monga_client.client.client import MongaClient
from monga_client.client.ws_client import WebSocketClient
from monga_client.client.monga import *
from monga_client.client.monga.file import FileAPI
from monga_client.client.monga.base import _do_request  
from Initialize import Initialize


if len(sys.argv) > 0 and len(sys.argv[2]) > 0:
    arg2 = sys.argv[2]

connect_config = configparser.ConfigParser()
connect_config.read(arg2)
action_config = configparser.ConfigParser()
action_config.read("action.conf")
'''
Log file format setting
'''

ws_lock = threading.Lock()
conn_dict_lock = threading.Lock()
modify_conn_dict_lock = threading.Lock()
token_dict_lock =threading.Lock()

logging.basicConfig(filename = 'connect.txt',
                    level = logging.DEBUG, filemode = 'a',
                    format = 
                    '[%(asctime)s] - [%(levelname)8s]: (%(threadName)-15s) %(message)s' ,
                    datefmt = '%Y-%m-%d %H:%M:%S')


class Connect(Initialize):

    def __init__(self):
        super().__init__()

        self.do_connect = action_config.get("action","connect")
        self.connect_token = action_config.get("action","connect_token")
        #self.update_token = action_config.get("action","update_token")
        self.user_number = int(connect_config.get("connect","connect_cnt"))
        self.stop_connect = connect_config.get("connect","connect_stop")
        self._do_request = _do_request
        self.connect_dict = {}
        

    def connect_server(self):
        token_str = ""
        token_dict = {}
        token_path = os.getcwd() + "/" + "token.txt"
        threads = []
        self.threads_name = []
        self.threads_name.append("MainThread")
        
        if os.path.exists(token_path) and sys.argv[1] == "Start":
            ct = threading.Thread(target = self.check_config, name = "Connect-cfg-thread")
            ct.start()
            self.threads_name.append(ct.getName())
            threads.append(ct)

            cgt = threading.Thread(target = self.get_token_dict, name = "Connect-token-dict")
            cgt.start()   
            self.threads_name.append(cgt.getName())
            threads.append(cgt)

            ctt = threading.Thread(target = self.check_total_thread, name = "Check-total-thread")
            self.threads_name.append(ctt.getName())
            ctt.start()
            threads.append(ctt)

            cuc = threading.Thread(target = self.check_url_connect, name = "Check-url_connect")
            self.threads_name.append(cuc.getName())
            cuc.start()
            threads.append(cuc)

            time.sleep(20)

            for i in range(1, self.user_number + 1):
                t = threading.Thread( target = self.ws_connect, args = [i], name = "Thread-" + str(i))
                time.sleep(0.05)
                t.start()
                self.threads_name.append(t.getName())
                threads.append(t)

            for x in threads:
                 x.join()
            time.sleep(1)

        elif sys.argv[1] == "Stop":
            connect_config.set("connect", "connect_stop", "yes")
            action_config.set("action", "connect", "no")
            f = open("connect.conf", 'w')
            connect_config.write(f)
            f.close()
            a = open("action.conf", 'w')
            action_config.write(a)
            a.close()
        else:
            print("token.txt not found !")

    def check_url_connect(self):
        while self.stop_connect == "no":
            time.sleep(60)

            try:
                req = urllib.request.Request(
                    'http://{0}:12345/list'.format(self._ip))
                res = urllib.request.urlopen(req)
            except urllib.error.URLError as error:
                logging.info('check_url_connect - {0}'.format(str(error.reason)))
                return
            except urllib.error.HTTPError as error:
                logging.info('check_url_connect - {0}'.format(str(error.reason)))
                return

            ws_accounts = res.read()
            conn_dict_lock.acquire()
            sum_conn = 0
            sum_disconn = 0 

            for i in range(1, self.user_number + 1):
                account = "\"test{0}\"".format(i)

                if not account in ws_accounts:
                    self.connect_dict[account] = False
                    sum_disconn += 1
                    logging.error('Url list show test%i not connect', i)
                else:
                    self.connect_dict[account] = True
                    sum_conn += 1

            conn_dict_lock.release()
            logging.info('Update url connect finish: %i users connect, %i users disconnect'
                , sum_conn, sum_disconn)

    def check_total_thread(self):
        while self.stop_connect == "no":
            time.sleep(150)
            active_count = threading.active_count()
            logging.info('Get total alive connect thread: %i', active_count)
            alive_class_list = threading.enumerate()
            alive_list = []

            for i in range(len(alive_class_list)):
                tmp = alive_class_list[i]
                tmp = tmp.getName()
                alive_list.append(tmp)

            for i in range(len(self.threads_name)):
                tmp = self.threads_name[i]

                if tmp not in alive_list:
                    try:
                        thread_num = int((tmp.lstrip("Thread-")))
                        logging.error('Thread %i is dead', thread_num)
                        self.restart_thread(thread_num)
                    except:
                        logging.error('Thread %s is dead', tmp)

    def restart_thread(self,i):
        t = threading.Thread( target = self.ws_connect, args = [i], name = "Thread-" + str(i))
        time.sleep(0.05)
        t.start()

    def get_token_dict(self):
        while self.stop_connect == "no":
            if self.connect_token == "yes":
                self.token_dictionary = {}
                f = open("token.txt", "r")

                for line in f:
                    token_str = (line.rstrip("\n")).split(" ")
                    self.token_dictionary[token_str[0]] = token_str[1]

                f.close()
                logging.info('Get token.txt to dictionary finish')
                action_config.set("action","connect_token","no")
                actionfile = open("action.conf", 'w')
                action_config.write(actionfile)
                actionfile.close()
                logging.info('modify action update token to no')
            time.sleep(30)

    def check_config(self):
        while self.stop_connect == "no":
            action_config.read("action.conf")
            self.do_connect = action_config.get("action","connect")
            self.connect_token = action_config.get("action","connect_token")
            connect_config.read(arg2)
            self.stop_connect = connect_config.get("connect","connect_stop")
            logging.info('Update connect config parameter finish ')

            if self.stop_connect == "yes":
                logging.info('Get connect stop = yes from config ')
            time.sleep(20)

    def ws_connect(self, i):
        _user = "test{0}".format(str(i))
        con_user = "\"" + _user + "\""

        token_dict_lock.acquire()
        try:
            my_token = self.token_dictionary[_user]
            logging.info('test{0} token is {1}'.format(i, my_token))
        except:
            logging.info("Connect thread - {0} failed to get token from token.txt".format(_user))
            return
        finally:
            token_dict_lock.release()
        ws = self.ws_connect_set(_user, my_token)

        if ws:
            ws_lock.acquire()
            ws.auth()
            ws_lock.release()

        connect_times = 0
        connect_count = 1

        while self.stop_connect == "no":
            time.sleep(120)
            conn_dict_lock.acquire()
            try:
                check_connect = self.connect_dict[con_user]

                if connect_count == connect_times and check_connect == True:
                    logging.info('{0} WebSocket connect {1} times'.format(_user, connect_count))
                    connect_count = connect_count + 1
            finally:
                conn_dict_lock.release()

            if not check_connect and self.do_connect == "yes":
                ws_lock.acquire()
                try:
                    ws.auth()
                    connect_times = connect_times + 1
                finally:
                    ws_lock.release()

               # check_connect = self.check_ws_connect(_user)
                # if  check_connect == True:
                #     modify_conn_dict_lock.acquire()
                #     try:
                #         self.connect_dict[con_user] = check_connect
                #     finally:
                #         modify_conn_dict_lock.release()
                #     logging.info('{0} WebSocket connect'.format(_user))
                # time.sleep(5)

    def ws_connect_set(self, user, token):
        ws = WebSocketClient(url = self.w_url,
                   token = token,
                   user = user,
                   domain = self._domain,
                   agent = '{0}.User.Portal'.format(user))
        return ws

    def check_ws_connect(self, user):
        try:
            req = urllib.request.Request(
                'http://{0}:12345/list'.format(self._ip))
            res = urllib.request.urlopen(req)
        except urllib.error.URLError as error:
            logging.info('check_ws_connect - {0}'.format(str(error.reason)))
            return
        except urllib.error.HTTPError as error:
            logging.info('check_ws_connect - {0}'.format(str(error.reason)))
            return

        ws_accounts = res.read()
        account = "\"{0}\"".format(user)

        if not account in ws_accounts:
            logging.error('{0} WebSocket disconnect'.format(user))
            return False
        else:
            return True

if __name__ == "__main__":
    if len(sys.argv) == 3:
        t = Connect()

        if (sys.argv[1] == "Start" or sys.argv[1] == "Stop") and ".conf" in sys.argv[2]:
            t.connect_server()
        else:
            print("Usage: connect.py Start/Stop connect.conf")
    else:
        print("Usage: connect.py Start/Stop connect.conf")
