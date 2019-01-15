from monga_client.common.utils import *

class ListAPI (object):

    def metadata(self, path = '', headers = {}) :
        _url = self.monga_url + '/'.join(['metadata', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def search_file(self, query, path = None, headers = {}) :
        if path :
            _url = self.monga_url + '/'.join(['search', path])
        else :
            _url = self.monga_url + '/'.join(['search'])
        _url = self.add_query_string(_url, {'query' : query})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def cursor(self, headers = {}) :
        _url = self.monga_url + '/'.join(['cursor'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def cursor_head(self, headers = {}) :
        _url = self.monga_url + '/'.join(['cursor'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'HEAD', _headers)

    def delta(self, cursor = None, last = None, event = True, 
              headers = {}) :
        if not cursor: cursor = current_timestamp()
        _url = self.monga_url + '/'.join(['delta'])
        _querys = {}
        if cursor :
            _querys['cursor'] = cursor
        if last :
            _querys['last'] = 1
        if event :
            _querys['event'] = 1
        _url = self.add_query_string(_url, _querys)
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def delta_get(self, cursor = None, last = None, headers = {}) :
        if not cursor: cursor = current_timestamp()
        _url = self.monga_url + '/'.join(['delta'])
        if cursor :
            _url = self.add_query_string(_url, {'cursor' : cursor})
        if last :
            _url = self.add_query_string(_url, {'last' : last})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

