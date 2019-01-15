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
from monga_client.client.monga.base import _do_request
from Initialize import Initialize


if len(sys.argv) > 0 and len(sys.argv[2]) > 0:
    arg2 = sys.argv[2]

delete_config = configparser.ConfigParser()
delete_config.read(arg2)
action_config = configparser.ConfigParser()
action_config.read("action.conf")

write_csv_lock = threading.Lock()
token_lock = threading.Lock()
delete_lock = threading.Lock()

'''
Log file format setting
'''
logging.basicConfig(filename = 'log.txt',
                    level = logging.DEBUG, filemode = 'a',
                    format = 
                    '[%(asctime)s] - [%(levelname)8s]: (%(threadName)-15s) %(message)s' ,
                    datefmt = '%Y-%m-%d %H:%M:%S')



class Delete(Initialize):

    def __init__(self):
        super().__init__()

        self._monga = MongaClient(self._monga_conf)
        self.do_delete = action_config.get("action","delete")
        self.update_token = action_config.get("action","update_token")
        self.user_number = int(delete_config.get("delete","delete_cnt"))
        self._upload_path = './upload_files'
        self.monga_url = self._fileop
        self._do_request = _do_request
        self.cond = threading.Condition()
        self.ready = False


    def file_delete(self):
        token_path = os.getcwd()+"/"+"token.txt"
        threads = []

        if os.path.exists(token_path) and sys.argv[1] == "Start":
            delete_file = os.listdir(self._upload_path)
            self.csv_file = "{0}_{1}_delete.csv".format(self.user_number, delete_file[0])
            if os.path.exists(self.csv_file):            # If file exists, delete it
                os.remove(self.csv_file)
                time.sleep(1)
            fd = open(self.csv_file, 'w')
            fd.close()

            super().get_token_dict()
            time.sleep(1)
            delete_start_time = time.time()

            for i in range(1, self.user_number + 1):
                t = threading.Thread( target = self.delete_thread, args = [i], name = "Thread-" + str(i))
                threads.append(t)
                t.start()

            self.cond.acquire()
            self.ready = True
            self.cond.notifyAll()
            self.cond.release()

            for x in threads:
                x.join()

            if len(self.token_dictionary) == 0:
                logging.info("File deletion is failed")
                return

            delete_end_time = time.time()
            delete_time = delete_end_time - delete_start_time
            logging.info('Total delete time: %s seconds.', delete_time)
        else:
            print("token.txt not found !")

    def delete_thread(self, i):
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
            logging.info("Delete thread - {0} failed to get token from token.txt".format(_user))
            return
        finally:
            token_lock.release()

        target_file = os.listdir(self._upload_path)
        target_path = target_file[0]
        delete_lock.acquire()
        self._monga.token = my_token
        res, respond_time = self._monga.delete_file(target_path)

        if (res is None):
            logging.info("Delete thread - File deletion is failed")
            return

        try:
            resp = res[0]['status']
        except:
            resp = res['status']

        if resp == 200:
            logging.info('%s deleted %s success.', _user, target_path)
        else:
            logging.error('%s deleted %s fail, status code is %s.', _user, target_path, resp)
        delete_lock.release()

        write_csv_lock.acquire()
        csv_fd = open(self.csv_file, 'a')
        line = str(i) + ', ' + str(respond_time) + '\n'
        csv_fd.write(line)
        csv_fd.close()   
        write_csv_lock.release()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        t = Delete()

        if (sys.argv[1] == "Start") and ".conf" in sys.argv[2]:
            if t.do_delete == 'yes':
                t.file_delete()
            else:
                print("In action.conf, delete needs to be yes.")
        else:
            print("Usage: delete.py Start delete.conf")
    else:
        print("Usage: delete.py Start delete.conf")



