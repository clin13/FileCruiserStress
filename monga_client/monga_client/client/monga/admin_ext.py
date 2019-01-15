import json

class AdminExtAPI():
    def admin_quota(self, tenant = None, token = None, headers = {}):
        _arr = ['admin','used']
        if tenant :
            _arr.append(self.quote(tenant))
        _url = self.monga_url + '/'.join(_arr)
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'GET', _headers)

    def admin_get_device(self, user = None, domain = None, token = None, 
                         headers = {}):
        _url = self.monga_url + '/'.join(['admin','device'])
        _query = {}
        if user : _query['user'] = user
        if domain : _query['domain'] = domain
        _url = self.add_query_string(_url, _query)
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'GET', _headers)

    def admin_enable_device(self, _id, token = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin','device', _id])
        _url = self.add_query_string(_url, {'enable' : 1})
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'PUT', _headers)

    def admin_disable_device(self, _id, token = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin','device', _id])
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'PUT', _headers)
        
    def admin_delete_device(self, _id, token = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin','device', _id])
        _url = self.add_query_string(_url, {'enable' : 1})
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'DELETE', _headers)

    def admin_clean_tenant(self, _id, token = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin','delete', _id])
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'DELETE', _headers)

    def admin_broadcast(self, msg = None, token = None, headers = {}):
        if msg:
            _req = {"message" : msg}
        else:
            _req = {}
        _url = self.monga_url + '/'.join(['admin','message'])
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'POST', _headers, json.dumps(_req))

    def admin_cache(self, user_id, token = None, once = False, headers = {}):
        _url = self.monga_url + '/'.join(['admin', 'cache', user_id])
        if once :
            _url = self.add_query_string(_url, {"once":1})
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        return self._do_request(_url, 'DELETE', _headers)
    
    def admin_add_team(self, _body, token = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin', 'team'])
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        _headers['Content-Type'] = 'application/json'
        return self._do_request(_url, 'POST', _headers, json.dumps(_body))

    def admin_update_team_meta(self, _body, token = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin', 'team_meta'])
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        _headers['Content-Type'] = 'application/json'
        return self._do_request(_url, 'POST', _headers, json.dumps(_body))

    def admin_change_team_name(self, _body, token = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin', 'team'])
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        _headers['Content-Type'] = 'application/json'
        return self._do_request(_url, 'PUT', _headers, json.dumps(_body))

    def admin_delete_team_member(self, tenant_id, user_id, token = None, 
                                 by_user = None, headers = {}):
        _url = self.monga_url + '/'.join(['admin', 'team', tenant_id, 'user',
                                          user_id])
        if by_user :
            _url = self.add_query_string(_url, {"by_user":by_user})
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        _headers['Content-Type'] = 'application/json'
        return self._do_request(_url, 'DELETE', _headers)

    def admin_get_activity(self, _id = None, _from = None, _to = None,
                           _tenant = None, _file = None, _pass = 0,
                           _sort = 1, token = None, headers = {}):
        if _id :
            _url = self.monga_url + '/'.join(['admin', 'activity', _id])
        else :
            _url = self.monga_url + '/'.join(['admin', 'activity'])
        _headers = headers.copy()
        _headers = self.set_token(token, _headers)
        if _from :
            _headers['X-Log-From'] = str(_from)
        if _to :
            _headers['X-Log-To'] = str(_to)
        if _tenant and _file:
            _headers['X-Tenant-Id'] = _tenant
            _headers['X-File-Name'] = _file
        _headers['X-Log-Pass'] = str(_pass)
        _headers['X-Log-Sort'] = str(_sort)
        return self._do_request(_url, 'GET', _headers)
