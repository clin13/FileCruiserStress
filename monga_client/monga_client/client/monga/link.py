import json

class LinkAPI (object):

    def share_get(self, headers = {}):
        _url = self.monga_url + '/'.join(['shares'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def share_put(self, _id, pwd = None, exp = None, search = None, 
                  headers = {}):
        _req = {}
        if pwd != None :
            _req['password'] = pwd
        if exp : 
            _req['expired_time'] = exp
        if search != None :
            _req['X-Link-Search'] = search
        _url = self.monga_url + '/'.join(['shares', _id])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'PUT', _headers, json.dumps(_req))

    def share_post(self, path, pwd = None, exp = None, search = True,
                   headers = {}):
        _url = self.monga_url + '/'.join(['shares', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        if pwd :
            _headers['X-Public-Password'] = pwd
        if exp :
            _headers['X-Expired-Time'] = exp
        _headers['X-Link-Search'] = search
        return self._do_request(_url, 'POST', _headers)

    def share_delete(self, _id, headers = {}):
        _url = self.monga_url + '/'.join(['shares', _id])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'DELETE', _headers)

    def share_search(self, body, headers = {}):
        _url = self.monga_url + '/'.join(['shares_search'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers, json.dumps(body))

    def direct_download(self, url, pwd = None, headers = {}):
        _headers = headers.copy()
        if pwd :
            _headers['X-Public-Password'] = pwd
        return self._do_request(url, 'GET', _headers)


