import os
import sys
import json
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

download_config = configparser.ConfigParser()
download_config.read(arg2)
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

MB = 1048576
mb = 1024000
KB = 1024
token_lock = threading.Lock()
download_lock = threading.Lock()

class Download(Initialize):

    def __init__(self):
        super().__init__()

        self._monga = MongaClient(self._monga_conf)
        self.do_download = action_config.get("action","download")
        self.update_token = action_config.get("action","update_token")
        self.user_number = int(download_config.get("download","download_cnt"))
        self._upload_path = './upload_files'
        self.monga_url = self._fileop
        self._do_request = _do_request
        self.cond = threading.Condition()
        self.ready = False

    def file_download(self):
        token_path = os.getcwd() + "/" + "token.txt"
        threads = []
        download_start_time = 0
        download_end_time = 0

        if os.path.exists(token_path) and sys.argv[1] == "Start":
            _download_file = os.listdir(self._upload_path)
            self.csv_file = "{0}_{1}_download.csv".format(self.user_number, _download_file[0])
            if os.path.exists(self.csv_file):            # If file exists, delete it
                os.remove(self.csv_file)
                time.sleep(1)
            fd = open(self.csv_file, 'w')
            fd.close()

            super().get_token_dict()
            time.sleep(1)
            download_start_time = time.time()

            for i in range(1, self.user_number + 1):
                t = threading.Thread( target = self.download_thread, args = [i], name = "Thread-" + str(i))
                threads.append(t)
                t.start()

            self.cond.acquire()
            self.ready = True
            self.cond.notifyAll()
            self.cond.release()

            for x in threads:
                x.join()

            download_end_time = time.time()
            download_time = download_end_time - download_start_time
            # Get file size
            total_MB = 0
            total_KB = 0
            file_list = os.listdir(self._upload_path)
            file_cnt = len(file_list)

            if file_cnt == 0 or len(self.token_dictionary) == 0:
                logging.info("File downloading is failed")
                return

            for x in range(file_cnt):
                single_file = file_list[x]
                f_path = self._upload_path + '/' + single_file
                f_size = os.path.getsize(f_path)
                if f_size >= MB:
                    mbs = f_size / MB
                    total_MB += mbs
                else:
                    kbs = f_size / KB
                    total_KB += kbs

            if total_MB > 0:
                logging.info('Download transfer rate: %s MB/s', (total_MB * self.user_number) / download_time)
            else:
                if (total_KB * self.user_number) / download_time > 1024:
                    logging.info('Download transfer rate: %s MB/s', ((total_KB * self.user_number) / download_time) / KB)
                else:
                    logging.info('Download transfer rate: %s KB/s', (total_KB * self.user_number) / download_time)

            logging.info('Total download time: %s seconds.', download_time)
            time.sleep(5)
        else:
            print("token.txt not found !")

    def check_file_in_server(self, target, token, download_path = '/'):
        meta_list = []
        self._monga.token = token
        meta_start = time.time()
        metadata = self._monga.metadata(path = download_path)
        meta_end = time.time()
        meta_Time = meta_end - meta_start
        metadata = json.loads(metadata[1])
        # print metadata
        for i in range(len(metadata['contents'])):
            meta_list.append(metadata['contents'][i]['path'][1:])
        if not target.decode() in meta_list:
            return -1
        return meta_Time

    def download_thread(self, i):
        self.cond.acquire()
        while not self.ready:
            self.cond.wait()
        self.cond.release()

        thread_start_time = time.time()
        _user = "test{0}".format(str(i))
        user_cnt = i
        token_lock.acquire()

        try:
            my_token = self.token_dictionary[_user]
        except:
            logging.info("Download thread - {0} failed to get token from token.txt".format(_user))
            return
        finally:
            token_lock.release()

        target_file = os.listdir(self._upload_path)
        file_count = len(target_file)

        for i in range(file_count):
            target_path = target_file[i]
            file_path = self._upload_path + '/' + target_path
            file_size = os.path.getsize(file_path)
            respond_time = 0

            try:
                meta_time = self.check_file_in_server(target_path, my_token)
                if meta_time == -1:
                    logging.info('{0} do not have file - {1}.'.format(_user, target_path))
                    return
            finally:
                if file_size <= MB:
                    download_lock.acquire()

                beg_time = time.time()
                resp, respond_time = self._monga.download_file(path = target_path)

                if (resp is None):
                    logging.info("Download thread - Download is failed")
                    return

                res_time = time.time() - beg_time
                if file_size <= MB:
                    download_lock.release()

                if resp[0]['headers']['content-length'] == file_size:
                    respond_time = res_time
            # resp,respond_time = self._monga.download_file(path=target_path)
            # download_lock.acquire()
            # try:
            #     resp,respond_time = self._monga.download_file(path=target_path)
            # finally:
            #     download_lock.release()
            normal = True

            try:
                res = resp[0]['status']
            except:
                res = resp['status']
                normal = False

            if res != 200:
                if normal == True:
                    logging.info('download response code is  %s and spend %s second', res, respond_time)
                else:
                    logging.info('download response code is  %s ', res)
            else:
                thread_end_time = time.time()
                thread_time = thread_end_time - thread_start_time
                logging.info('%s spent %s seconds to download. Thread time: %s', _user, respond_time, thread_time)

            csv_fd = open(self.csv_file, 'a')
            line = str(user_cnt) + ', ' + str(respond_time) + ', ' + str(meta_time) + '\n'
            csv_fd.write(line)
            time.sleep(0.1)
            csv_fd.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        t = Download()

        if sys.argv[1] == "Start" and ".conf" in sys.argv[2]:
            if t.do_download == 'yes':
                t.file_download()
            else:
                print("In action.conf, download needs to be yes.")
        else:
            print("Usage: download.py Start download.conf")
    else:
        print("Usage: download.py Start download.conf")
