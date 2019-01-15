import pika
import json

class PikaClient(object):

    def __init__(self, log, conf):
        #self.io_loop       = io_loop
        self.connected     = False
        self.connecting    = False
        self.connection    = None
        self._channel      = None
        self.server_host   = conf.get('amqp_host', '127.0.0.1')
        self.server_port   = int(conf.get('amqp_port', 5672))
        self.user_name     = conf.get('amqp_user', 'guest')
        self.user_pwd      = conf.get('amqp_pwd', 'guest')
        self.EXCHANGE      = conf.get('amqp_exchange_name', 'message')
        self.EXCHANGE_TYPE = conf.get('amqp_exchange_type', 'fanout')
        self.QUEUE         = conf.get('amqp_queue_name', 'test')
        self.ROUTING_KEY   = conf.get('amqp_routing_key', 'key')
        self.log = log

    def timeout_func(self):
        self.connection.close()
    
    def publish_msg(self, msg):
        try:
            msg = json.dumps(msg)
            param = pika.ConnectionParameters(
                host = self.server_host,
                port = self.server_port,
                virtual_host = '/',
                credentials = pika.PlainCredentials(self.user_name,
                                                    self.user_pwd))
            properties = pika.BasicProperties(
                            content_type='application/json', delivery_mode=1)
            self.connection = pika.BlockingConnection(param)
            self.connection.add_timeout(10, self.timeout_func)
            channel = self.connection.channel()
            channel.queue_declare(queue = self.QUEUE, 
                                  durable = False, 
                                  exclusive = False, 
                                  auto_delete = False)
            channel.confirm_delivery()
            if self.EXCHANGE != '':
                channel.exchange_declare(exchange = self.EXCHANGE,
                                         exchange_type = self.EXCHANGE_TYPE)
            if channel.basic_publish(exchange = self.EXCHANGE,
                                     routing_key = self.ROUTING_KEY,
                                     body = msg,
                                     properties = properties) :
                self.log.info('Broadcast Message')
            self.connection.close()
        except Exception as err:
            self.log.error(err)
        return
