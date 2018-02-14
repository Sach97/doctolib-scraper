# -*- coding: utf-8 -*-
# import scrapy


# class DoctolibspiderSpider(scrapy.Spider):
#     name = 'doctolibspider'
#     allowed_domains = ['doctolib.fr']
#     start_urls = ['http://doctolib.fr/']

#     def parse(self, response):
#         pass

import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DoctolibItem
from ..pipelines import DoctolibPipeline
from lxml import html

class DoctolibspiderSpider(CrawlSpider):
    name = 'doctolibspider'
    allowed_domains = ['doctolib.fr']
    start_urls = (
        'https://www.doctolib.fr/pediatre/paris',
    )

    rules = (Rule(LinkExtractor(allow=(), restrict_css='body > div.results > div > div.col-8.col-padding.search-results-col-list > div.pagination-links > div.next > a'), callback="parse_names", follow= True),)

    def filterPostal(self,string):
        return re.search(r'-?\d+\.?\d*',string).group(0)
    
    def parse_names(self,response):
        names = response.css('a > div::text').extract()
        postals = response.css('div.dl-search-result-content > div.dl-text-body > div::text').extract()[1::2]
        newpostals = [self.filterPostal(x) for x in postals]
        status = response.css("div.dl-search-result-title > div.dl-search-result-subtitle::text").extract()
        convention = response.css("div.dl-search-result-content > div.dl-search-result-regulation-sector::text").extract()
        for n,p,s,c in zip (names,newpostals,status,convention):
            item = DoctolibItem()
            item['name'] = n
            item['postal'] = p
            item['status'] = s
            item['convention'] = c
            yield item
            #print({'name': n,'postal':p})
        # for n in names:
        #     print({'name': n})