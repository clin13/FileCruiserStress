import json

class CommentAPI (object):

    def comment_post(self, path, msg = '', headers = {}):
        _url = self.monga_url + '/'.join(['fileops', 'comment', 
                                          self.quote(path)])
        body = json.dumps({'msg' : msg})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers, body)

    def comment_get(self, path, headers = {}):
        _url = self.monga_url + '/'.join(['fileops', 'comment', 
                                          self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def comment_put(self, _id, msg = 'test', headers = {}):
        _url = self.monga_url + '/'.join(['fileops', 'comment', 
                                          self.quote(_id)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        body = json.dumps({'msg' : msg})
        return self._do_request(_url, 'PUT', _headers, body)
        
    def comment_delete(self, _id, headers = {}):
        _url = self.monga_url + '/'.join(['fileops', 'comment', 
                                          self.quote(_id)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'DELETE', _headers)
        
    def comment_search(self, body, headers = {}):
        _url = self.monga_url + '/'.join(['fileops', 'comment_search'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers, json.dumps(body))


