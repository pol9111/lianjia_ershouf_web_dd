# -*- coding: utf-8 -*-
import random


BOT_NAME = 'lianjia_ershouf_web'

SPIDER_MODULES = ['lianjia_ershouf_web.spiders']
NEWSPIDER_MODULE = 'lianjia_ershouf_web.spiders'


CONCURRENT_REQUESTS = 50
# DOWNLOAD_DELAY = random.random()

USER_AGENT = ''
COOKIES_ENABLED = True
# COOKIES_DEBUG = True

DOWNLOADER_MIDDLEWARES = {
   'lianjia_ershouf_web.middlewares.RandomUserAgentMiddleware': 450,
   # 'lianjia_ershouf_web.middlewares.RandomProxyMiddleware': 750,
}


ITEM_PIPELINES = {
   'lianjia_ershouf_web.pipelines.MongoPipeline': 300,
   # 'scrapy_redis.pipelines.RedisPipeline': 900,  # 数据保存到redis里
}


MONGO_URI = 'localhost'
MONGO_DATABASE = 'lianjia'


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PARAMS = {
    'db': 0,
    'password': 'qwe123',
}




PROXY_URL = ''
PROIES = 'proies'


# 去重类，要使用Bloom Filter请替换DUPEFILTER_CLASS
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# 散列函数的个数，默认为6，可以自行修改
BLOOMFILTER_HASH_NUMBER = 6
# Bloom Filter的bit参数，默认30，占用128MB空间，去重量级1亿
BLOOMFILTER_BIT = 30

# 使用了scrapy_redis_bloomfilter里的调度器组件，不使用scrapy默认的调度器
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
# 使用队列形式
SCHEDULER_QUEUE_CLASS = "scrapy_redis_bloomfilter.queue.SpiderQueue"
# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True