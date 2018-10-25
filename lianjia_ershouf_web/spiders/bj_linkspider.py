# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import redis
from lianjia_ershouf_web.settings import REDIS_HOST, REDIS_PORT, REDIS_PARAMS


class ErshoufSpider(RedisSpider):
    name = 'bj_link'
    allowed_domains = ['bj.lianjia.com']
    REDIS_CONN = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password='qwe123', db=REDIS_PARAMS['db'], decode_responses=True)

    redis_key = "bj_ershouf_region:start_urls"
    base_url = 'https://bj.lianjia.com/'
    cache = [] # 记录已经抓取过的地区

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'bj.lianjia.com',
            'Pragma': 'no-cache',
            'Referer': 'https://bj.lianjia.com/',
            'Upgrade-Insecure-Requests': '1',
        }
    }

    def parse(self, response):
        """请求所有大区域"""
        b_region_list = response.xpath('//div[@class="sub_nav section_sub_nav"]/a/@href').extract()
        for url in b_region_list:
            yield scrapy.Request(url=self.base_url+url, callback=self.request_s_region)

    def request_s_region(self, response):
        """请求所有小区域"""
        s_region_list = response.xpath('//div[@class="sub_sub_nav section_sub_sub_nav"]/a/@href').extract()
        for url in s_region_list:
            if url not in self.cache:
                yield scrapy.Request(url=self.base_url+url, callback=self.create_url)

    def create_url(self, response):
        """构造本小区域, 所有列表页请求"""
        total_page = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').re_first('"totalPage":(\d+)')
        # cur_page = response.xpath('//div[@class="page-box fr"]').re_first('"curPage":(\d+)')
        # region = response.xpath('//div[@class="page-box fr"]').re_first('page-url="/ershoufang/(.*?)pg{page}/"')
        base_url = response.url
        if total_page:
            for page in range(1, int(total_page)+1):
                self.REDIS_CONN.lpush('bj_ershouf:start_urls', base_url + 'pg' +str(page) + '/')
        else:
            self.REDIS_CONN.lpush('bj_ershouf:start_urls', response.url)