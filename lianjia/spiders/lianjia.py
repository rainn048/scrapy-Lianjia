# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:38:12 2017

@author: LEE
"""

import scrapy
import re
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
			
        page = response.xpath("//div[@class='page-box house-lst-page-box'][@page-data]").re("\d+")
        p = re.compile(r'[^\d]+')
        #这里是判断有没有下一页，毕竟不是所有区都是有第100页的，不能for循环到100
        if len(page)>1 and page[0] != page[1]:
            next_page = p.match(response.url).group()+str(int(page[1])+1)
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            
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