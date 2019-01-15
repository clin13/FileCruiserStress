import os
import sys
import time
import logging
import configparser
import threading
from threading import *
from threading import Thread, current_thread
from monga_client.client.client import MongaClient
from monga_client.client.monga import *
from Initialize import Initialize


if len(sys.argv) > 0 and len(sys.argv[2]) > 0:
    arg2 = sys.argv[2]

trash_config = configparser.ConfigParser()
trash_config.read(arg2)
action_config = configparser.ConfigParser()
action_config.read("action.conf")

'''
Log file format setting
'''
logging.basicConfig(filename = 'log.txt',
                    level = logging.DEBUG, filemode = 'a',
                    format = 
                    '[%(asctime)s] - [%(levelname)8s]: (%(threadName)-15s) %(message)s' ,
                    datefmt = '%Y-%m-%d %H:%M:%S')

token_lock = threading.Lock()
trash_lock = threading.Lock()

class Trash(Initialize):

    def __init__(self):
        super().__init__()

        self._monga = MongaClient(self._monga_conf)
        self.do_trash = action_config.get("action","trash")
        self.update_token = action_config.get("action","update_token")
        self.user_number = int(trash_config.get("trash","trash_cnt"))
        self._upload_path = './upload_files'
        self.monga_url = self._fileop
        self.cond = threading.Condition()
        self.ready = False


    def file_trash(self):
        token_path = os.getcwd() + "/" + "token.txt"
        threads = []

        if os.path.exists(token_path) and sys.argv[1] == "Start":
            super().get_token_dict()
            time.sleep(1)
            for i in range(1, self.user_number + 1):
                t = threading.Thread( target = self.trash_thread, args = [i], name = "Thread-" + str(i))
                threads.append(t)
                t.start()

            self.cond.acquire()
            self.ready = True
            self.cond.notifyAll()
            self.cond.release()

            for x in threads:
                x.join()

            if len(self.token_dictionary) == 0:
                logging.info("Moving file to trash can is failed")
                return
        else:
            print("token.txt not found !")

    def trash_thread(self, i):
        self.cond.acquire()
        while not self.ready:
            self.cond.wait()
        self.cond.release()

        _user = "test{0}".format(str(i))
        user_cnt = i
        token_lock.acquire()
        try:
            my_token = self.token_dictionary[_user]
        except:
            logging.info("Trash thread - {0} failed to get token from token.txt".format(_user))
            return
        finally:
            token_lock.release()

        target_file = os.listdir(self._upload_path)
        target_path = target_file[0]
        trash_lock.acquire()
        self._monga.token = my_token
        result = self._monga.trash_get(team = _user)

        if (result is None):
            logging.info("Trash thread - Moving file to trash can is failed")
            return

        if result[0]['status'] == 200:
            logging.info('%s got file list of trash can.', _user)
        else:
            logging.info('%s got file list of trash can failed. Status: %s', _user, result[0]['status'])

        res, respond_time = self._monga.trash_delete(_id = None, team = _user)

        try:
            resp = res[0]['status']
        except:
            resp = res['status']

        if resp == 200:
            logging.info('%s emptied trash can.', _user)
        else:
            logging.info('%s emptied trash can failed. Status: %s', _user, resp)
        trash_lock.release()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        t = Trash()

        if (sys.argv[1] == "Start") and ".conf" in sys.argv[2]:
            if t.do_trash == 'yes':
                t.file_trash()
            else:
                print("In action.conf, trash needs to be yes.")
        else:
            print("Usage: trash.py Start trash.conf")
    else:
        print("Usage: trash.py Start trash.conf")