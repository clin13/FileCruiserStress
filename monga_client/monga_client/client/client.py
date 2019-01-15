import http.client
import json
from urllib.parse import urljoin, parse_qs, urlsplit, urlunsplit, urlparse, quote, urlencode
import mimetypes
import os
from os.path import basename
from monga_client.common.utils import *
from monga_client.client.ks_client import KeystoneClient
from monga_client.client.license import LicenseClient
from monga_client.client.content_search import ContentSearchClient
from monga_client.client.monga import *
from monga_client.client.monga.base import _do_request
from monga_client.client.swift.proxy import SwiftProxy
import logging

class MongaClient(AdminExtAPI, AccountAPI, ListAPI, FileAPI, TrashAPI,
                  CommentAPI, LinkAPI, ShareAPI, TeamAPI, JagabeeAPI,
                  SwiftProxy, FavoriteAPI, LicenseClient,
                  ContentSearchClient, PreviewAPI):

    def __init__(self, config):
        self.monga_url = config.get('monga_url',
                                    'http://127.0.0.1:7000/v1/')
        self.auth_url = config.get('auth_url', 
                                   'http://127.0.0.1:5000/v3/')
        self.ws_url = config.get('ws_url', 
                                 'http://127.0.0.1:12345/')
        self.swift_url = config.get('swift_url', 
                                    'http://127.0.0.1:8080/v1/')
        self.license_url = config.get('license_url', 
                                    'http://127.0.0.1:7777/')
        self.frog_url = config.get('frog_url',
                                    'http://127.0.0.1:5555/')
        self.content_search_url = config.get('content_search_url', 
                                    'http://127.0.0.1:11111/v1/content_search')
        self.auth_user = config.get('auth_user', 'admin')
        self.auth_tenant = config.get('auth_tenant', 'admin')
        self.auth_password = config.get('auth_password', '0985123123')
        self.auth_domain = config.get('auth_domain', 'Default')
        self._do_request = _do_request
        self.set_auth_client()
        self.token = None

    def quote(self, name):
        return quote(name)

    def set_monga_url(self, url):
        self.monga_url = url

    def set_auth_url(self, url):
        self.auth_url = url
        self.set_auth_client()

    def set_token(self, token, headers):
        _headers = headers.copy()
        if not token :
            _token = self.token
        else :
            _token = token
        _headers['X-Auth-Token'] = _token
        return _headers

    def set_auth_client(self):
        self.ks = KeystoneClient(path   = self.auth_url,
                                 admin  = self.auth_user,
                                 pwd    = self.auth_password,
                                 tenant = self.auth_tenant,
                                 domain = self.auth_domain)
        
    def authenticate(self, user = None, pwd = None, tenant = None, 
                     domain = None):
        if not user : 
            user = self.auth_user
        if not pwd :
            pwd = self.auth_password
        if not tenant :
            tenant = self.auth_tenant
        if not domain :
            domain = self.auth_domain
        self.token = self.ks.get_token(user, pwd, tenant, domain)

    def get_tenant_id(self):
        return self.ks.get_tenant_by_name(self.auth_user, self.token)[0]['id']

    def get_user_id(self):
        return self.ks.get_user(self.auth_user, self.token)[0]['id']

    def add_query_string(self, url, param):
        new_param = {}
        for k, v in param.items() :
            if v == None : continue
            if type(v) == 'unicode' :
                new_param[k] = v.encode('utf-8')
            else :
                new_param[k] = v
        param = new_param
        _param = urlencode(param)
        _url = url.endswith('&') and (url + _param) or (url + '?' + _param)
        return _url

    def ws_list(self, headers = {}):
        _url = self.ws_url + 'list'
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)

