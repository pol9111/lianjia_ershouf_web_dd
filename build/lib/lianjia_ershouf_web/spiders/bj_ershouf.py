# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from lianjia_ershouf_web.items import LianjiaErshoufWebItem
from scrapy_redis.spiders import RedisCrawlSpider


class ErshoufSpider(RedisCrawlSpider):
    name = 'bj_ershouf'
    allowed_domains = ['bj.lianjia.com']

    redis_key = "bj_ershouf:start_urls"

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

    rules = [
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="page-box house-lst-page-box"]')), # 动态生成
        Rule(LinkExtractor(restrict_xpaths='//li[@class="clear LOGCLICKDATA"]//div[@class="title"]'), callback='item_parse'),
    ]

    def item_parse(self, response):
        el0 = response.xpath('//div[@class="title-wrapper"]')
        el1 = response.xpath('//div[@class="overview"]/div[@class="content"]')
        el2 = response.xpath('//div[@class="base"]/div[@class="content"]/ul')
        el3 = response.xpath('//div[@class="transaction"]/div[@class="content"]/ul')
        item = LianjiaErshoufWebItem()
        # 右上信息
        for data in el0:
            item['title'] = data.xpath('.//h1[@class="main"]/text()').extract_first(default='')
            item['follow'] = data.xpath('.//span[@id="favCount"]/text()').extract_first(default='')
            item['view'] = data.xpath('.//span[@id="cartCount"]/text()').extract_first(default='')
        for data in el1:
            item['link_id'] = data.xpath('./div[4]/div[4]/span[@class="info"]/text()').extract_first(default='')
            item['community'] = data.xpath('.//div[@class="communityName"]/a[1]/text()').extract_first(default='')
            item['address'] = data.xpath('.//div[@class="areaName"]/a/text()').extract_first(default='')
            item['age'] = data.xpath('.//div[@class="area"]/div[@class="subInfo"]/text()').re_first(r'(\d+)年建/', default='')
            item['totalPrice'] = data.xpath('.//span[@class="total"]/text()').extract_first(default='')
            item['unitPrice'] = data.xpath('.//div[@class="area"]/div[@class="mainInfo"]/text()').extract_first(default='')
        # 基本属性
        for data in el2:
            item['houseType'] = data.xpath('./li[1]/text()').extract_first(default='')
            item['floor'] = data.xpath('./li[2]/text()').extract_first(default='')
            item['all_area'] = data.xpath('./li[3]/text()').extract_first(default='')
            item['structure'] = data.xpath('./li[4]/text()').extract_first(default='')
            item['inner_area'] = data.xpath('./li[5]/text()').extract_first(default='')
            item['architecturalType'] = data.xpath('./li[6]/text()').extract_first(default='')
            item['orientation'] = data.xpath('./li[7]/text()').extract_first(default='')
            item['buildingStructure'] = data.xpath('./li[8]/text()').extract_first(default='')
            item['decorationSituation'] = data.xpath('./li[9]/text()').extract_first(default='')
            item['ladder'] = data.xpath('./li[10]/text()').extract_first(default='')
            item['heatingMode'] = data.xpath('./li[11]/text()').extract_first(default='')
            item['elevators'] = data.xpath('./li[12]/text()').extract_first(default='')
            item['propertyAge'] = data.xpath('./li[13]/text()').extract_first(default='')
        # 交易属性
        for data in el3:
            item['listingTime'] = data.xpath('./li[1]/span[2]/text()').extract_first(default='')
            item['tradingRights'] = data.xpath('./li[2]/span[2]/text()').extract_first(default='')
            item['lastTransaction'] = data.xpath('./li[3]/span[2]/text()').extract_first(default='')
            item['houseUsage'] = data.xpath('./li[4]/span[2]/text()').extract_first(default='')
            item['ageLimit'] = data.xpath('./li[5]/span[2]/text()').extract_first(default='')
            item['propertyBelong'] = data.xpath('./li[6]/span[2]/text()').extract_first(default='')
            item['mortgageInfo'] = data.xpath('./li[7]/span[2]/text()').extract_first(default='').strip()
            item['paper'] = data.xpath('./li[8]/span[2]/text()').extract_first(default='')
        yield item