import os
import sys
import time
import random
import logging
import datetime
import threading
from threading import Thread, current_thread
from threading import *
import configparser
from monga_client.client.ks_client import KeystoneClient
from monga_client.client.client import MongaClient
from monga_client.client.ws_client import WebSocketClient
from Initialize import Initialize


action_cfg = configparser.ConfigParser()
action_cfg.read("action.conf")

if len(sys.argv) > 0:
    arg2 = sys.argv[2]

token_config = configparser.ConfigParser()
token_config.read(arg2)
'''
Log file format setting
'''
if sys.argv[1] == "Start":
    logging.basicConfig(filename = 'log.txt',
                        level = logging.DEBUG, filemode = 'w',
                        format = 
                        '[%(asctime)s] - [%(levelname)8s]: (%(threadName)-10s) %(message)s' ,
                        datefmt = '%Y-%m-%d %H:%M:%S')


class Token(Initialize):

    def __init__(self):
        super().__init__()
        self.stop_token = token_config.get("token", "token_stop")
        self.total_user = int(token_config.get("token", "token_cnt"))
        self.RefreshDuration = int(token_config.get("token", "token_RefreshDuration"))

    def create_token(self):
        token_dict = {}
        self.token_path = os.getcwd() + "/" + "token.txt"
        threads = []

        if sys.argv[1] == "Start":
            if os.path.exists(self.token_path):            # If file exists, delete it
                os.remove(self.token_path)
                time.sleep(1)

            # Create two threads, one always reads token.conf, another is getting token.
            ct = threading.Thread(target = self.check_config, name = "Cfg-Thread")
            threads.append(ct)
            ct.start()

            t = threading.Thread(target = self.get_token_to_file, name = "Thread-Token" )
            threads.append(t)
            t.start()

            for x in threads:
                x.join()

        elif sys.argv[1] == "Stop":
            token_config.set("token", "token_stop", "yes")
            tokenfile = open("token.conf", 'w')
            token_config.write(tokenfile)
            tokenfile.close()

    def check_config(self):
        while self.stop_token == "no":
            token_config.read(arg2)
            self.stop_token = token_config.get("token", "token_stop")

            if self.stop_token == "no":
                if sys.argv[1] == "Stop":
                    break
            if self.stop_token == "yes":
                break
            time.sleep(20)

    def get_token_to_file(self):
        count = 0
        get_token_start_time = 0
        get_token_end_time = 0

        while self.stop_token == "no":
            get_token_end_time = time.time()
            duration  = get_token_end_time - get_token_start_time

            if count == 0 or duration > self.RefreshDuration :
                action_cfg.set("action","update_token","yes")
                actionfile = open("action.conf", 'w')
                action_cfg.write(actionfile)
                logging.info('Updating token.')
                actionfile.close()
                get_token_start_time = time.time()
                token_dict = {}
                f =  open(self.token_path, "w")

                for i in range(self.total_user):
                    _user = "test{0}".format(i + 1)
                    _monga = MongaClient(self._monga_conf)
                    _monga.authenticate(user = _user,
                                        pwd = self._password,
                                        tenant = _user,
                                        domain = self._domain)

                    if _monga.token is None:
                        logging.info("{0} failed to get token".format(_user))
                        return

                    token_dict[_user] = _monga.token
                    f.write(_user + " " + token_dict[_user] + "\n")
                    logging.info('Got test%s token: %s', (i+1), _monga.token)

                action_cfg.set("action","update_token","no")
                action_cfg.set("action","connect_token","yes")
                actionfile = open("action.conf", 'w')
                action_cfg.write(actionfile)
                logging.info('Update token finished.')
                actionfile.close()
                f.close()
                get_token_start_time = time.time()
                count += 1
            time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        t = Token()

        if (sys.argv[1] == "Start" or sys.argv[1] == "Stop") and ".conf" in sys.argv[2]:
            t.create_token()
        else:
            print("Usage: token1.py Start token.conf")
    else:
        print("Usage: token1.py Start token.conf")
