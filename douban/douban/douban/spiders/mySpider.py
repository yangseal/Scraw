#coding=utf-8
'''
PyTools:PyCharm 2017.1
Python :Python3.5
Author :colby_chen
CreDate:2017-04-13
'''
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban.items import doubanItem
'''爬取准备
*目标网站：豆瓣电影TOP250
*目标网址：http://movie.douban.com/top250
*目标内容：
    *豆瓣电影TOP250部电影的以下信息
    *电影名称
    *电影信息
    *电影评分
*输出结果：生成csv文件
'''
class Douban(CrawlSpider):
    name = "doubanMovie"
    redis_key='douban:start_urls'
    start_urls=['http://movie.douban.com/top250']
    url='http://movie.douban.com/top250'
    def parse(self,response):
        item=doubanItem()
        selector=Selector(response)
        Movies=selector.xpath('//div[@class="info"]')
        print('Movies',Movies)
        for eachMoive in Movies:
            print('eachMoive',eachMoive)
            title=eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle=''
            print('title',title)
            for each in title:
                fullTitle+=each
                print('eachtitle', each)
            movieInfo=eachMoive.xpath('div[@class="bd"]/p/text()').extract()
            star=eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            quote=eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote=quote[0]
            else:
                quote=''
            print('fullTitle',fullTitle)
            print('movieInfo', movieInfo)
            print('star', star)
            print('quote', quote)
            item['title']=fullTitle
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            yield item
        nextLink=selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextLink:
            nextLink=nextLink[0]
            print(nextLink)
            yield Request(self.url+nextLink,callback=self.parse)