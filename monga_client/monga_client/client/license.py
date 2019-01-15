import json

class LicenseClient (object):

    def add_license_conn(self, user, domain) :
        _url = self.license_url + 'record'
        _body = {
            'user_name' : user,
            'domain'    : domain
        }
        _url = self.add_query_string(_url, _body)
        return self._do_request(_url, 'POST')

    def remove_license_conn(self, user, domain) :
        _url = self.license_url + 'record'
        _body = {
            'user_name' : user,
            'domain'    : domain
        }
        _url = self.add_query_string(_url, _body)
        return self._do_request(_url, 'DELETE')

