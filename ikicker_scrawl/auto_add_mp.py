# -*- coding: utf-8 -*-
#添加指定公众号到爬虫数据库

# 导入包

from wechatsogou import *

import datetime
import time
import logging
import logging.config

# 日志
logging.config.fileConfig('auto_add_mp_logging.conf')
logger = logging.getLogger()

# 搜索API实例
wechats = WechatSogouApi()

#数据库实例
mongo = mongo('upload')
add_list = mongo.query('wx_account')
succ_count = 0

for add_item in add_list :
    try:
        if add_item['wx_hao']:
            where_sql = {'wx_hao':add_item['wx_hao']}
            mp_data   = mongo.query('wx_mp_info', where_sql)
            print(mp_data.count())
            if mp_data.count()==0:
                wechat_info = wechats.get_gzh_info(add_item['wx_hao'])
                if(wechat_info != ""):
                    mongo.insert('wx_mp_info', {'wx_name': wechat_info['name'], 'wx_hao': wechat_info['wechatid'],
                    'company': wechat_info['renzhen'],'description': wechat_info['jieshao'], 'logo_url': wechat_info['img'],
                    'qr_url': wechat_info['qrcode'], 'wz_url': wechat_info['url'],'last_qunfa_id': 0, 'last_qufa_time': 0, 'rank_article_count': 0,
                    'rank_article_release_count': 0, 'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))})
            else:
                print(u"已经存在的公众号")
        elif add_item['wx_name']:
            '''获取对应信息  通过姓名获取信息'''
            wechat_infos = wechats.search_gzh_info(add_item['name'].encode('utf8'))
            for wx_item in wechat_infos:
                '''公众号数据写入数据库 搜索一下是否已经存在'''
                where_sql = {'wx_hao': wx_item['wechatid']}
                mp_data   = mongo.query('wx_mp_info',where_sql)
                if mp_data.count()==0:
                    mongo.insert('wx_mp_info', {'wx_name': wechat_info['name'], 'wx_hao': wechat_info['wechatid'],
                                                'company': wechat_info['renzhen'], 'description': wechat_info['jieshao'], 'logo_url': wechat_info['img'],
                                                'qr_url': wechat_info['qrcode'], 'wz_url': wechat_info['url'],
                                                'last_qunfa_id': 0, 'last_qufa_time': 0, 'rank_article_count': 0,
                                                'rank_article_release_count': 0, 'create_time': time.strftime("%Y-%m-%d %H:%M:%S",
                                                                             time.localtime(time.time()))})
                else:
                    print(u"已经存在的公众号")
        #删除已添加项
        mongo.delete('wx_account', {'wx_name':add_item['wx_name'],'wx_hao':add_item['wx_hao']})
    except:
        print(u"出错，继续")
        continue
print("get Wechat success")

    

