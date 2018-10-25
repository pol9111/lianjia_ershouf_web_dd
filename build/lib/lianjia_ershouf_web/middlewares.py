# -*- coding: utf-8 -*-
import base64
import random
from fake_useragent import UserAgent
from lianjia_ershouf_web.proxypool import proxy_handler


class RandomUserAgentMiddleware(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    @classmethod
    def from_settings(cls, settings):
        return cls(settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', UserAgent().random)


class RandomProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = proxy_handler.take_proxy()
        request.meta['proxy'] = proxy['https']