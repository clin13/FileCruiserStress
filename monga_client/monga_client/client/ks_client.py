import http.client
import json
from urllib.parse import urlparse
import urllib
import logging
from monga_client.common.retry import retry_auth
from monga_client.common.exception import *
from monga_client.common.utils import *
log = logging.getLogger(__name__)

class KeystoneClient():

    def __init__(self, path = 'http://127.0.0.1:35357/v3/', admin = 'admin', 
                 pwd = 'admin', tenant = 'admin', domain = 'Default'):
        self.admin_name = admin
        self.admin_pwd = pwd
        self.admin_tenant = tenant
        self.domain_name = domain
        self.token = ''
        self.path = path

    @retry_auth(ClientUnauthorizedError, tries=3)
    def verify_token(self, verify_token, admin_token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if admin_token :
            self.token = admin_token
        _url = self.path + 'auth/tokens'
        headers = {'X-Auth-Token' : self.token, 
                   'X-Subject-Token' : verify_token}
        return self._do_request(_url, headers = headers)

    @retry_auth(ClientUnauthorizedError, tries=3)
    def update_user(self, user_id, _body, admin_token = None, 
                        reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if admin_token :
            self.token = admin_token
        _url = self.path + 'users/' + user_id
        headers = {
            'X-Auth-Token' : self.token,
            'Content-Type' : 'application/json'
        }
        return self._do_request(_url, 
                                method = 'PATCH', 
                                headers = headers,
                                body = json.dumps(_body),)

    @retry_auth(ClientUnauthorizedError, tries=3)        
    def get_tenant(self, tenant_id, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'projects/' + tenant_id
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['project']

    @retry_auth(ClientUnauthorizedError, tries=3)        
    def get_roles(self, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'roles'
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['roles']

    @retry_auth(ClientUnauthorizedError, tries=3)
    def get_domain(self, domain_id, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'domains/' + domain_id
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['domain']

    @retry_auth(ClientUnauthorizedError, tries=3)
    def get_domain_list(self, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'domains'
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)

    @retry_auth(ClientUnauthorizedError, tries=3)
    def get_tenant_by_name(self, tenant_name, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'projects?name=' + \
                   urllib.quote(tenant_name.encode('utf-8'))
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['projects']

    @retry_auth(ClientUnauthorizedError, tries=3)        
    def get_user_by_id(self, user_id, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'users/' + user_id
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['user']

    @retry_auth(ClientUnauthorizedError, tries=3)        
    def get_user(self, user_name, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'users?name=' + \
                   urllib.quote(user_name.encode('utf-8'))
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['users']

    @retry_auth(ClientUnauthorizedError, tries=3)
    def get_tenant_user_roles(self, user_id, tenant_id, token = None, 
                              reauth = False):
        #/tenants/{tenant_id}/users/{user_id}/roles
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _path = self.path.replace('v3','v2.0',1)
        _url = self.path + 'projects/' + tenant_id + \
               '/users/' + user_id+ '/roles'
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)

    @retry_auth(ClientUnauthorizedError, tries=3)
    def get_user_tenants(self, user_id, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _url = self.path + 'users/' + user_id+ '/projects'
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['projects']
        
    @retry_auth(ClientUnauthorizedError, tries=3)
    def get_tenant_users(self, tenant_id, token = None, reauth = False):
        if reauth :
            self.token = self.get_admin_token()
        if token :
            self.token = token
        _path = self.path.replace('v3','v2.0',1)
        _url = _path + 'tenants/' + tenant_id+ '/users'
        headers = {'X-Auth-Token' : self.token}
        return self._do_request(_url, headers = headers)['users']

    def get_token(self, user, pwd, tenant, domain, reauth = False) :
        _url = self.path + 'auth/tokens'
        auth_body = {
            "auth" : {
                "identity" : {
                    "methods" : ["password"],
                    "password" : {
                        "user" : {
                            "domain" : {
                                "name" : domain
                            },
                            "name" : user,
                            "password" : pwd
                        }
                    }
                },
                "scope" : {
                    "project" : {
                        "domain" : {
                            "name" : domain
                        },
                    "name" : tenant}
                }
            }
        }
        headers = {'Content-Type' : 'application/json'}
        return self._do_request(_url, 
                                method = 'POST', 
                                headers = headers,
                                body = json.dumps(auth_body),
                                token = True)

    @retry_auth(ClientUnauthorizedError, tries=3)
    def get_admin_token(self, reauth = False) :
        return self.get_token(self.admin_name, self.admin_pwd,
                              self.admin_tenant, self.domain_name)

    @staticmethod
    def _do_request(url, method = 'GET', headers = None, body = None, 
                        token = False):
        _u = urlparse(url)
        if _u.scheme == 'http' :
            conn = http.client.HTTPConnection(_u.hostname, _u.port, timeout = 10)
        elif _u.scheme == 'https' :
            conn = http.client.HTTPConnection(_u.hostname, _u.port, timeout = 10)

        #Make size header
        if body :
            headers['Content-Length'] = len(body)
        _url = _u.path + '?' + _u.query
        conn.request(method, _url, body, headers)
        resp = conn.getresponse()
        _headers = {}
        for header, value in resp.getheaders():
            _headers[header] = value
        _resp = AttributeDict({'status' : resp.status, 'headers' : _headers})
        _body = resp.read()
        if _resp.status >= 200 and _resp.status < 300:
            if token :
                return _resp.headers.get('x-subject-token')
            else :
                return json.loads(_body)
        elif _resp.status == 401 :
            raise ClientUnauthorizedError(_body)
        elif _resp.status >= 400 and _resp.status < 500 :
            raise ClientBadRequestError(_body)
        else :
            raise ClientInternalServerError(_body)
