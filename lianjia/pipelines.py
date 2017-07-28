# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        with open("lianjia.txt",'a') as fp:
            fp.write(item['title']+'@'+item['price']+'@'+item['communityName']+'@'+item['areaName']+'\n')
