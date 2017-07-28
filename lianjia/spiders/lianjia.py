# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:38:12 2017

@author: LEE
"""

import scrapy
from lianjia.items import LianjiaItem

class QuotesSpider(scrapy.Spider):
    name = "lianjia"

    start_urls = [
        'https://bj.lianjia.com/ershoufang/',
    ]

    def parse(self, response):
        #urls  = response.xpath("body/div/div/ul/li/div/div//a/attribute::href").extract()
        urls = response.xpath("//ul[@class='sellListContent']/li/a/attribute::href").extract()
        for each_url in urls:
            yield scrapy.Request(each_url, self.parse_detail_page)
            
            
    def parse_detail_page(self, response):
        baseInfo ={}
        item = LianjiaItem()
        item['title'] = response.xpath("//h1[@class='main']/text()").extract_first()
        item['price'] = response.xpath("//div[@class='price ']/span[@class='total']/text()").extract_first()
        item['communityName']=response.xpath("//div[@class='communityName']/a[@class='info']/text()").extract_first()
        item['areaName']=response.xpath("//div[@class='areaName']/span[@class='info']/a/text()").extract_first()
        
        basea = response.xpath("//div[@class='content']/ul/li")
        for each in basea:
            label = each.xpath("./span/text()").extract_first()
            value = each.xpath("./text()").extract_first()
            baseInfo[label]=value
        
        more = response.xpath("//div[@class='introContent showbasemore']/div")
        for each in more[0:-2]:
            label = each.xpath("./div[@class='name']/text()").extract_first()
            print(label)
            value = each.xpath("./div[@class='content']/text()").extract_first()
            print(value)
            baseInfo[label]=value
        item['base']=baseInfo
		
        yield item