import os
import sys
import json
import time
import logging
import configparser
import threading
from threading import *
from threading import Thread, current_thread
from monga_client.client.ks_client import KeystoneClient
from monga_client.client.client import MongaClient
from monga_client.client.ws_client import WebSocketClient
from monga_client.client.monga import *
from monga_client.client.monga.base import _do_request
from Initialize import Initialize


if len(sys.argv) > 0 and len(sys.argv[2]) > 0:
    arg2 = sys.argv[2]

upload_config = configparser.ConfigParser()
upload_config.read(arg2)
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
upload_lock = threading.Lock()

class Upload(Initialize, MongaClient):

    def __init__(self):
        super().__init__()

        self._monga = MongaClient(self._monga_conf)
        self.do_upload = action_config.get("action","upload")
        self.update_token = action_config.get("action","update_token")
        self.user_number = int(upload_config.get("upload","upload_cnt"))
        self._upload_path = './upload_files'
        self.monga_url = self._fileop
        self._do_request = _do_request
        self.cond = threading.Condition()
        self.ready = False

    def file_upload(self):
        token_path = os.getcwd() + "/" + "token.txt"
        threads = []
        upload_start_time = 0
        upload_end_time = 0

        if os.path.exists(token_path) and sys.argv[1] == "Start":
            upload_file = os.listdir(self._upload_path)
            self.csv_file = "{0}_{1}.csv".format(self.user_number, upload_file[0])

            if os.path.exists(self.csv_file):            # If file exists, delete it
                os.remove(self.csv_file)
                time.sleep(1)
            fd = open(self.csv_file, 'w')
            fd.close()

            super().get_token_dict()
            time.sleep(1)
            upload_start_time = time.time()

            for i in range(1, self.user_number + 1):
                t = threading.Thread(target = self.upload_thread, args = [i], name = "Thread-" + str(i))
                threads.append(t)
                t.start()

            self.cond.acquire()
            self.ready = True
            self.cond.notifyAll()
            self.cond.release()

            for x in threads:
                x.join()

            upload_end_time = time.time()
            upload_time = upload_end_time - upload_start_time
            # Get file size
            total_MB = 0
            total_KB = 0
            file_list = os.listdir(self._upload_path)
            file_cnt = len(file_list)

            if file_cnt == 0 or len(self.token_dictionary) == 0 or upload_time == 0:
                logging.info("File uploading is failed")
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
                logging.info('Upload transfer rate: %s MB/s', (total_MB * self.user_number) / upload_time)
            else:
                if (total_KB * self.user_number) / upload_time > 1024:
                    logging.info('Upload transfer rate: %s MB/s', ((total_KB * self.user_number) / upload_time) / KB)
                else:
                    logging.info('Upload transfer rate: %s KB/s', (total_KB * self.user_number) / upload_time)

            logging.info('Total upload time: %s seconds.', upload_time)
            time.sleep(5)

        elif sys.argv[1] == "Stop":
            upload_config.set("upload", "upload_stop", "yes")
            f = open("upload.conf", 'w')
            upload_config.write(f)
            f.close()
        else:
            print("token.txt not found !")

    def upload_file(self, path, body = 'test', file_path = None, headers = {}, token = None) :
        _url = self.monga_url + '/'.join(['files', super().quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = token

        if file_path :
            _size = os.path.getsize(file_path)
            try:
                _f = open(file_path, 'rb')
                time_beg = time.time()
                _resp, _body =  self._do_request(_url, 'POST', _headers, _f, _size = _size)
                respond_time = time.time() - time_beg
                res_list = []
                tmp_resp = dict(_resp)
                tmp_resp = tmp_resp["status"]
                res_list.append(tmp_resp)
                res_list.append(respond_time)

                return res_list

            except Exception as err:
                logging.error('upload file exception error %s ', err)
            finally:
                _f.close()
        else :
            time_beg = time.time()
            res = self._do_request(_url, 'POST', _headers, body)
            respond_time = time.time()-time_beg

            return res,respond_time

    def chunked_upload(self, path, file_path, body = None, _id = None, offset = None,
                       headers = {}, token = None):
        _url = self.monga_url + '/'.join(['chunked_upload', path])

        if _id and offset :
            _url = self.add_query_string(_url, {'upload_id' : _id,
                                                'offset' : offset})
        if not body :
            body = ''.join(['a' for i in range(mb)])

        _headers = headers.copy()
        _headers['X-Auth-Token'] = token
        _headers['X-File-Path'] = file_path.decode('utf-8').encode('utf-8')
        _headers['X-File-Size'] = str(len(body))
        time_beg = time.time()
        res = self._do_request(_url, 'POST', _headers, body)
        respond_time = time.time() - time_beg

        return res,respond_time

    def commit_chunked_upload(self, path, _id, _size = 0, headers = {}, token = None):
        _url = self.monga_url + '/'.join(['commit_chunked_upload', 
                                          self.quote(path)])
        _url = self.add_query_string(_url, {'upload_id' : _id})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = token
        _headers['X-File-Size'] = str(_size)
        time_beg = time.time()
        res = self._do_request(_url, 'POST', _headers)
        respond_time = time.time() - time_beg

        return res,respond_time

    def check_config(self):
        while self.stop_upload == "no":
            action_config.read("action.conf")
            self.update_token = action_config.get("action","update_token")
            time.sleep(5)

    def check_file_in_server(self, target_file, token, upload_path = '/'):
        meta_list = []
        self._monga.token = token
        meta_start = time.time()
        metadata = self._monga.metadata(path = upload_path)
        meta_end = time.time()
        meta_Time = meta_end - meta_start
        metadata = json.loads(metadata[1])
        # print metadata
        for i in range(len(metadata['contents'])):
            meta_list.append(metadata['contents'][i]['path'][1:])
        target = target_file

        if not target.decode() in meta_list:
            logging.info('file:{0} not in server'.format(target))

        return meta_Time

    def upload_thread(self, i):
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
            logging.info("Upload thread - {0} failed to get token from token.txt".format(_user))
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

            if file_size <= MB:
                upload_lock.acquire()
                try:
                    resp = self.upload_file(path = target_path, body = 'test', file_path = file_path, token = my_token)
                finally:
                    upload_lock.release()

                if (resp is None):
                    logging.info("Upload thread - upload is failed")
                    return

                if resp[0] != 200:
                    logging.info('upload response code is  %s and spend %s second', resp[0], resp[1])
                else:
                    thread_end_time = time.time()
                    thread_time = thread_end_time - thread_start_time
                    logging.info('%s spent %s seconds to upload. Thread time: %s', _user, resp[1], thread_time)

                meta_time = self.check_file_in_server(target_path, my_token)
                csv_fd = open(self.csv_file, 'a')
                line = str(user_cnt) + ', ' + str(resp[1]) + ', ' + str(meta_time) + '\n'
                csv_fd.write(line)
                time.sleep(0.1)
                csv_fd.close()
            else:
                fd = open(file_path,'rb')
                upload_times = file_size / mb

                if file_size % mb != 0:
                    upload_times += 1
                i = 0

                while i <= upload_times:
                    _body = fd.read(mb)

                    if i == 0:
                        _resp, n_respound_time = self.chunked_upload(
                            path = target_path, file_path = file_path, body = _body, token = my_token)

                        if (_resp is None):
                            logging.info("Upload thread - Chunk upload is failed")
                            return

                        resp = _resp[1]
                        respond_time = respond_time + n_respound_time
                    elif i == upload_times:
                        _resp, n_respound_time = self.chunked_upload(
                            path = target_path, file_path = file_path, body = _body, token = my_token)
                        fd.close()
                        u_res, n_respound_time = self.commit_chunked_upload(
                            path = target_path, _id = r_id, _size = r_size, token = my_token)
                        respond_time = respond_time + n_respound_time

                        thread_end_time = time.time()
                        thread_time = thread_end_time - thread_start_time
                        logging.info('%s spent %s seconds to upload. Thread time: %s', _user, respond_time, thread_time)

                        meta_time = self.check_file_in_server(target_path, my_token)    # Get metadata
                        csv_fd = open(self.csv_file, 'a')
                        line = str(user_cnt) + ', ' + str(respond_time) + ', ' + str(meta_time) + '\n'
                        csv_fd.write(line)
                        time.sleep(0.1)
                        csv_fd.close()

                        return u_res, respond_time
                    else:
                        _resp,n_respound_time = self.chunked_upload(
                            path = target_path, file_path = file_path, body = _body, _id = r_id, offset = r_size, token = my_token)
                        resp = _resp[1]
                        respond_time = respond_time + n_respound_time

                    resp = json.loads(str(resp))
                    r_id = resp['upload_id']
                    r_size = resp['offset']
                    i += 1

if __name__ == "__main__":
    if len(sys.argv) == 3:
        t = Upload()

        if (sys.argv[1] == "Start" or sys.argv[1] == "Stop") and ".conf" in sys.argv[2]:
            if t.do_upload == 'yes':
                t.file_upload()
            else:
                print('In action.conf, upload needs to be yes.')
        else:
            print("Usage: upload.py Start/Stop upload.conf")
    else:
        print("Usage: upload.py Start/Stop upload.conf")
