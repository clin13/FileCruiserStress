class TeamAPI (object):

    def team_scope_post(self, path, user_id, headers = {}):
        _url = self.monga_url + '/'.join(['team_scope', path])
        _url = self.add_query_string(_url, {'user_id' : user_id})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def team_scope_get(self, path, headers = {}):
        _url = self.monga_url + '/'.join(['team_scope', path])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def team_scope_delete(self, path, user_id, headers = {}):
        _url = self.monga_url + '/'.join(['team_scope', path])
        _url = self.add_query_string(_url, {'user_id' : user_id})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'DELETE', _headers)

    def team_log_get(self, team, headers = {}):
        _url = self.monga_url + '/'.join(['team_log'])
        _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def team_user_list(self, path = None, headers = {}):
        if path :
            _url = self.monga_url + '/'.join(['team_user', path])
        else :
            _url = self.monga_url + '/'.join(['team_user'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def role_table(self, headers = {}):
        _url = self.monga_url + '/'.join(['role'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def team_permission(self, team, headers = {}):
        _url = self.monga_url + '/'.join(['permission'])
        _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)
