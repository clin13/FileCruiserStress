import json

class ShareAPI (object):

    def share_file_post(self, user, path, write = True, domain_id = None, 
                        desc = '', team = None, headers = {}):
        _req = {
            'permission' : {'write' : write},
            'file_path' : path,
            'description' : desc
        }
        if user :
            _req['user'] = user
        if team :
            _req['team'] = team
        if domain_id :
            _req['domain_id'] = domain_id
        _url = self.monga_url + '/'.join(['fileops','share_file'])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers, json.dumps(_req))
    
    def share_file_put(self, _id, write = True, desc = None, headers = {}):
        _req = {
            'permission' : {'write' : write},
        }
        if desc :
            _req['description'] = desc
        _url = self.monga_url + '/'.join(['fileops','share_file', _id])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'PUT', _headers, json.dumps(_req))

    def share_file_get(self, team = 'admin', headers = {}):
        _url = self.monga_url + '/'.join(['fileops','share_file'])
        _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def share_file_delete(self, _id, headers = {}):
        _url = self.monga_url + '/'.join(['fileops','share_file', _id])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'DELETE', _headers)

    def get_confirm_list(self, team = 'admin', headers = {}):
        _url = self.monga_url + '/'.join(['fileops','confirm'])
        _url = self.add_query_string(_url, {'team' : team})
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

    def confirm_share_file(self, _id, headers = {}):
        _url = self.monga_url + '/'.join(['fileops','confirm', _id])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'POST', _headers)

    def deny_share_file(self, _id, headers = {}):
        _url = self.monga_url + '/'.join(['fileops','confirm', _id])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'DELETE', _headers)


