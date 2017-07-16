# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item

class NovelItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookName=Field()
    bookTile=Field()
    chapterNum=Field()
    chapterName=Field()
    chapterURL=Field()
