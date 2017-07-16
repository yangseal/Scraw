#coding=utf-8
'''
Tools:PyCharm 2017.1
Py:Python3.5
Author:colby_chen
Date:2017-04-13
'''
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector, HtmlXPathSelector
from novel.items import NovelItem
class novSpider(CrawlSpider):
    name="novelspider"
    redis_key="novelspider:start_urls"
    start_urls=['http://www.daomubiji.com']

    def parse_item_content(self, response):
        sell = Selector(response)
        #从上一层URL获取字典
        item = response.meta['item']
        #解析article标签下所有小说内容
        data=sell.xpath('//article[@class="article-content"]')
        item['content'] = data.xpath('string(.)').extract()[0]
        #提交入库
        yield item

    def parse_item(self, response):
        sell = Selector(response)
        title=sell.xpath('/html/body/div[1]/div/h1/text()').extract()[0]
        print('title',title)
        desc = sell.xpath('/html/body/div[1]/div/div/text()').extract()[0]
        print('desc',desc)
        sites = sell.xpath('/html/body/section/div[2]/div/article/a')
        print('sites', sites)
        item={}
        for site in sites:
            print(site)
            item['title']=title
            item['desc'] = desc
            item['zhangjieurl']=site.xpath('@href').extract()[0]
            item['zhangjie'] = site.xpath('text()').extract()[0]
            print('字典item[zhangjieurl]',item['zhangjieurl'])
            #将下一层URL和本函数的字典参数传递给parse_item_content函数
            yield Request(item['zhangjieurl'], meta={'item':item},callback=self.parse_item_content)
    def parse(self,response):
        selector=Selector(response)
        article = selector.xpath('//article/p/a')
        items=[]
        for each in article:
            #print('each',each)
            url = each.xpath('@href').extract()[0]
            items.append(url)
        print(items)
        for item in items:
            yield Request(item, callback=self.parse_item)