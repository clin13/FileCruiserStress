class TrashAPI (object):

    def trash_get(self, team = 'admin', headers = {}) :
        _url = self.monga_url + '/'.join(['fileops', 'trash'])
        _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def trash_post(self, path, headers = {}) :
        _url = self.monga_url + '/'.join(['fileops', 'trash', 
                                          self.quote(path)])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def trash_delete(self, _id, team, headers = {}) :
        if _id :
            _url = self.monga_url + '/'.join(['fileops', 'trash', _id])
        else :
            _url = self.monga_url + '/'.join(['fileops', 'trash'])
        _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        res = self._do_request(_url, 'DELETE', _headers)
        respond_time = 10
        return res, respond_time

    def trash_put(self, _id, team, headers = {}) :
        _url = self.monga_url + '/'.join(['fileops', 'trash', _id])
        _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'PUT', _headers)


