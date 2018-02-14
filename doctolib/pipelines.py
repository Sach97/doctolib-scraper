# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class DoctolibPipeline(object):
    def process_item(self, item, spider):
        if item['status'] == "Pédiatre":
            return item
        else:
            raise DropItem("Not a pediatre in %s" % item)