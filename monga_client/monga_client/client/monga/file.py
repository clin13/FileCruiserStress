import os
import time

class FileAPI (object):

    def upload_file(self, path, body = 'test', file_path = None, headers = {}) :
        _url = self.monga_url + '/'.join(['files', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        if file_path :
            _size = os.path.getsize(file_path)
            try:
                _f = open(file_path, 'rb')
                time_beg = time.time()
                _resp, _body =  self._do_request(_url, 'POST', _headers, _f, 
                                                 _size = _size)
                respond_time = time.time()-time_beg
                return _resp, respond_time
            except Exception as err:
                print(err)
            finally:
                _f.close()
        else :
            time_beg = time.time()
            res = self._do_request(_url, 'POST', _headers, body)
            respond_time = time.time()-time_beg
            return res,respond_time

    def download_file(self, path, headers = {}) :
        _url = self.monga_url + '/'.join(['files', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        time_beg = time.time()
        res = self._do_request(_url, 'GET', _headers)
        respond_time = time.time()-time_beg
        return res,respond_time

    def bulk_download_file(self, body, headers = {}) :
        _url = self.monga_url + '/'.join(['bulk_download'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers, body)

    def get_thumbnail(self, path, headers = {}) :
        _url = self.monga_url + '/'.join(['thumbnail', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def create_folder(self, path, headers = {}) :
        _url = self.monga_url + '/'.join(['fileops', 'create_folder'])
        _url = self.add_query_string(_url, {'path' : path})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def copy_file(self, _from, _to, headers = {}) :
        _url = self.monga_url + '/'.join(['fileops', 'copy'])
        _url = self.add_query_string(_url, {'from_path' : _from,
                                            'to_path' : _to})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def revisions(self, path, headers = {}):
        _url = self.monga_url + '/'.join(['revisions', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def restore(self, path, rev, headers = {}):
        _url = self.monga_url + '/'.join(['restore', self.quote(path)])
        _url = self.add_query_string(_url, {'rev' : rev})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def move_file(self, _from, _to, headers = {}) :
        _url = self.monga_url + '/'.join(['fileops', 'move'])
        _url = self.add_query_string(_url, {'from_path' : _from,
                                            'to_path' : _to})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def delete_file(self, path, headers = {}) :
        _url = self.monga_url + '/'.join(['fileops', 'delete'])
        _url = self.add_query_string(_url, {'path' : path})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        time_beg = time.time()
        res = self._do_request(_url, 'POST', _headers)
        respond_time = time.time()-time_beg
        return res,respond_time

    def chunked_upload(self, path, file_path, body = None, _id = None, offset = None,
                       headers = {}):
        _url = self.monga_url + '/'.join(['chunked_upload', path])
        if _id and offset :
            _url = self.add_query_string(_url, {'upload_id' : _id,
                                                'offset' : offset})
        if not body :
            body = ''.join(['a' for i in range(1024000)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        _headers['X-File-Path'] = file_path#.decode('utf-8').encode('utf-8')
        _headers['X-File-Size'] = str(len(body))
        time_beg = time.time()
        res = self._do_request(_url, 'POST', _headers, body)
        respond_time = time.time()-time_beg
        return res,respond_time

    def commit_chunked_upload(self, path, _id, _size = 0, headers = {}):
        _url = self.monga_url + '/'.join(['commit_chunked_upload', 
                                          self.quote(path)])
        _url = self.add_query_string(_url, {'upload_id' : _id})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        _headers['X-File-Size'] = str(_size)
        time_beg = time.time()
        res = self._do_request(_url, 'POST', _headers)
        respond_time = time.time()-time_beg
        return res,respond_time

    def lock_post(self, path, headers = {}):
        _url = self.monga_url + '/'.join(['lock', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def lock_delete(self, path, headers = {}):
        _url = self.monga_url + '/'.join(['lock', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'DELETE', _headers)
