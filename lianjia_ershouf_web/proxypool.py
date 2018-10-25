import random
import redis
import requests
from lianjia_ershouf_web.settings import PROXY_URL, PROIES, REDIS_HOST, REDIS_PORT, REDIS_PARAMS


class ProxyHandler(object):

    def __init__(self, redis_conn):
        self.redis_conn = redis_conn

    def get_proxy(self):
        html = requests.get(PROXY_URL).json()
        ips = html.get('msg')
        for dic in ips:
            ip = dic.get('ip')
            port = dic.get('port')
            ip_port = {'https': 'http://' + ip + ':' + port}
            self.redis_conn.lpush(PROIES, ip_port)

    def take_proxy(self):
        proxy_list = self.redis_conn.lrange(PROIES, 0, -1)
        proxy = random.choice(proxy_list)
        return proxy

    def update_proxy(self):
        self.redis_conn.delete(PROIES)
        self.get_proxy()


REDIS_CONN = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_PARAMS['db'], decode_responses=True)
proxy_handler = ProxyHandler(REDIS_CONN)