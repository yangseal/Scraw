# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MongoDBPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGODB_DB']]  # 获得数据库的句柄
        self.postItem = self.db[settings['MONGODB_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        print('postItem',postItem)
        self.postItem.insert_one(postItem)  # 向数据库插入一条记录
        yield item  # 会在控制台输出原item数据，可以选择不写