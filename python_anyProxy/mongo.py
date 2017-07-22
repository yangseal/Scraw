#coding=utf8

import settings
from pymongo import MongoClient

class mongo():
    """数据库类 """

    #数据库初始化配置
    def __init__(self):
        self.host = settings.host
        self.user = settings.user
        self.passwd = settings.passwd
        self.db = settings.db
        self.port = settings.port
        self.__conn()

    #数据库连接
    def __conn(self):
        self.client   = MongoClient(
            'mongodb://' + self.user + ':' + self.passwd + '@' + self.host + ':' + self.port + '/' + self.db)
        return self


    def __query(self, collection, cond):
        return self.client.upload[collection].find(cond)

    def __insert(self,collection, cond):
        self.client.upload[collection].insert(cond)

    def __delete(self, collection, cond):
        self.client.upload[collection].remove(cond)

    def __update(self, collection, cond, sql):
        self.client.upload[collection].update(cond,{'$set':sql})

    #数据查询操作
    def query(self, collection, cond={}):
        return self.__query(collection, cond)

    #数据插入操作
    def insert(self, collection, cond={}):
        self.__insert(collection, cond)

    #数据删除操作
    def delete(self, collection, cond={}):
        self.__delete(collection, cond)

    #数据库更新操作
    def update(self, collection, cond, result):
        self.__update(collection, cond, result)

if __name__=='__main__':
    pass