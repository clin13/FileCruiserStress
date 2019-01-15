import json

class FavoriteAPI (object):

    def favorite_post(self, path, headers = {}):
        _url = self.monga_url + '/'.join(['favorite', self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def favorite_get(self, headers = {}):
        _url = self.monga_url + '/'.join(['favorite'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)
        
    def favorite_delete(self, _id = None, path = None, headers = {}):
        _url = self.monga_url + '/'.join(['favorite'])
        query = {}
        if _id :
            query['id'] = _id
        if path :
            query['path'] = path
        _url = self.add_query_string(_url, query)
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'DELETE', _headers)
        
