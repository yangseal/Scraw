# -*- coding: utf-8 -*-

#from . import config
from pymongo import MongoClient
from . import config

class DbException(Exception):
    """数据库 异常 基类
    """
    pass


class MongoDbException(DbException):
    """数据库 Mongodb 异常类
    """
    pass



class mongo():
    """数据库类 """

    #数据库初始化配置
    def __init__(self,db):
        self.host = config.host
        self.user = config.user
        self.passwd = config.passwd
        self.db = db
        self.port = config.port
        self.__conn()

    #数据库连接
    def __conn(self):
        self.client   = MongoClient()
        self.client   = MongoClient(
            'mongodb://' + self.user + ':' + self.passwd + '@' + self.host + ':' + self.port + '/' + self.db)
        return self


    def __query(self, collection, cond):
        return self.client.upload[collection].find(cond)

    def __insert(self,collection, cond):
        self.client.upload[collection].insert(cond)

    def __delete(self, collection, cond):
        self.client.upload[collection].remove(cond)

    def __update(self, collection, cond, result):
        self.client.upload[collection].update(cond, {'$set':result})

    #数据查询操作
    def query(self, collection, cond ={}):
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


if __name__ == '__main__':
    pass
