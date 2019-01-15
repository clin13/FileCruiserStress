class AccountAPI (object):

    def get_user_info(self, headers = {}) :
        _url = self.monga_url + '/'.join(['account'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def update_user(self, body, headers = {}) :
        _url = self.monga_url + '/'.join(['account'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'PUT', _headers, body)

    def get_usage(self, team = None, headers = {}):
        _url = self.monga_url + '/'.join(['usage'])
        if team :
            _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)


