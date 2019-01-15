import configparser
import time

config = configparser.ConfigParser()
config.read("StressTest.conf")
action_config = configparser.ConfigParser()
action_config.read("action.conf")

class Initialize():

    def __init__(self):
        self._ip = config.get("setting","ip")
        self._domain = config.get("setting","domain")
        self._password = config.get("setting","password")
        self.w_url = 'ws://{0}'.format(self._ip)
        self._fileop = 'http://{0}/fileop/v1/'.format(self._ip)
        self._ks = 'http://{0}/keystone/v3/auth/tokens'.format(self._ip)
        # MongaClient init value
        self._auth_url = 'http://{0}/keystone/v3/'.format(self._ip)
        self._ws_url= 'http://{0}:12345/'.format(self._ip)
        self._swift_url = 'http://{0}:8080/v1/'.format(self._ip)
        self._license_url = 'http://{0}:7777/'.format(self._ip)
        self._content_search_url = 'http://{0}:9200/v1/content_search'.format(self._ip)
        self._monga_conf={'monga_url':self._fileop,'auth_url':self._auth_url,
                            'ws_url':self._ws_url,'swift_url':self._swift_url,
                            'license_url':self._license_url,
                            'content_search_url':self._content_search_url,
                            'auth_user':'admin','auth_tenant':'admin',
                            'auth_password':'0985123123','auth_domain':'Default'}

    def get_token_dict(self):
        while self.update_token == "yes":
            time.sleep(1)
            action_config.read("action.conf")
            self.update_token = action_config.get("action","update_token")

        self.token_dictionary = {}
        f = open("token.txt", "r")

        for line in f:
            token_str = (line.rstrip("\n")).split(" ")
            self.token_dictionary[token_str[0]] = token_str[1]

        f.close()
        time.sleep(5)

