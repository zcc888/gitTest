# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mycwpjt.items import MycwpjtItem

#显示可用的模板              scrapy genspider -l
#利用crawlspider创建的框架  scrapy genspider -t crawl weisun sohu.com
#开始爬取                   scrapy crawl weisun --nolog

class WeisunSpider(CrawlSpider):
    name = 'weisun'
    allowed_domains = ['sohu.com']
    start_urls = ['http://sohu.com/']

    rules = (
        # 新闻网页的url地址类似于：
        # “http://news.sohu.com/20160926/n469167364.shtml”
        # 所以可以得到提取的正则表达式为'.*?/n.*?shtml’
        Rule(LinkExtractor(allow=('.*?/n.*?shtml'), allow_domains=('sohu.com')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = MycwpjtItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # 根据Xpath表达式提取新闻网页中的标题
        i["name"] = response.xpath("/html/head/title/text()").extract()
        # 根据Xpath表达式提取当前新闻网页的链接
        i["link"] = response.xpath("//link[@rel='canonical']/@href").extract()
        return i
