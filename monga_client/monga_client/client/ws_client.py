from websocket import create_connection
import json
from monga_client.common.timeout import *

class WebSocketClient():

    def __init__(self, url, token = None, user = None, domain = None,
                 agent = None):
        self.url = url
        self.conn = None
        self.token = token
        self.user = user
        self.domain = domain
        self.agent = agent

    #@timeout(1)
    def connect(self, url = None):
        if url :
            self.conn = create_connection(url)
        else :
            self.conn = create_connection(self.url)

    def close(self):
        self.conn.close()

    #@timeout(3)
    def auth(self, token = None, user = None, domain = None, agent = None):
        if not self.conn : self.connect()
        self.auth_body = {
            'auth' : {
                'token'  : token or self.token,
                'user'   : user or self.user,
                'domain' : domain or self.domain,
                'agent'  : agent or self.agent
            }
        }
        self.send_msg(json.dumps(self.auth_body))

    #@timeout(3)
    def recv_msg(self) :
        if not self.conn : self.connect()
        return self.conn.recv()

    #@timeout(3)
    def send_msg(self, msg):
        if not self.conn : self.connect()
        self.conn.send(msg)
