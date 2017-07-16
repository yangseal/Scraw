# -*- coding: utf-8 -*-
# 查找公众号最新文章

from wechatsogou.tools import *
from wechatsogou import *
import datetime
import time
import logging
import logging.config

# 日志
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

# 搜索API实例
wechats = WechatSogouApi()

# 数据库实例
mongo = mongo('upload')

# 循环获取数据库中所有公众号
mp_list = mongo.query('wx_mp_info')
succ_count = 0

now_time = datetime.datetime.today()
now_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0)

for item in mp_list:
    try:
        #查看一下该号今天是否已经发送文章
        last_qunfa_id   = item['last_qunfa_id']
        last_qunfa_time = item['last_qufa_time']
        cur_qunfa_id    = last_qunfa_id
        wz_url = ""
        if 'wz_url' in item:
            wz_url = item['wz_url']
        else:
            wechat_info = wechats.get_gzh_info(item['wx_hao'])
            if not 'url' in wechat_info:
                continue
            wz_url = wechat_info['url']
        print(item['wx_name'])
        # 获取最近文章信息
        wz_list = wechats.get_gzh_message(url=wz_url)
        if u'链接已过期' in wz_list:
            wechat_info = wechats.get_gzh_info(item['wx_hao'])
            if not 'url' in wechat_info:
                continue
            wz_url = wechat_info['url']
            wz_list = wechats.get_gzh_message(url=wz_url)
            mongo.update('wx_mp_info', {'wx_hao': item['wx_hao']}, {'wz_url': wechat_info['url'], 'logo_url': wechat_info['img'],
                          'qr_url': wechat_info['qrcode']})
        #type==49表示是图文消息
        qunfa_time = ''
        for wz_item in wz_list:
            temp_qunfa_id = int(wz_item['qunfa_id'])
            if (last_qunfa_id == temp_qunfa_id):
                print("----没有需要更新的文章－－－－－")
                break
            if (cur_qunfa_id < temp_qunfa_id):
                cur_qunfa_id = temp_qunfa_id
                qunfa_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(wz_item['datetime']))
            succ_count += 1
            if wz_item['type'] == '49':
                # 把文章写入数据库
                # 更新文章条数
                if not wz_item['content_url']:
                    continue
                article_info = wechats.deal_article(url=wz_item['content_url'])
                print(article_info)
                if not article_info:
                    continue
                if not article_info['yuan']:
                    pass
                sourceurl = wz_item['source_url']
                mongo.insert('wx_wenzhang_info', {
                    'wx_name'    : item['wx_name'], 'title'          : wz_item['title'],
                    'source_url' : sourceurl, 'content_url'          : wz_item['content_url'],
                    'cover_url'  : wz_item['cover'],  'description'  : wz_item['digest'],
                    'date_time'  : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(wz_item['datetime'])),
                    'mp_id'      : item['_id'],   'author'           : wz_item['author'],
                    'msg_index'  : wz_item['main'],  'copyright_stat': wz_item['copyright_stat'],
                    'qunfa_id'   : wz_item['qunfa_id'], 'type'       : wz_item['type'],
                    'data'       : {'like_count' : 0, 'read_count' : 0, 'comment_count': 0}
                })
            print('update success')
        # 更新最新推送ID
        if (last_qunfa_id < cur_qunfa_id):
            where_sql = {'wx_name': item['wx_name']}
            mongo.update('wx_mp_info', where_sql, {
                'last_qunfa_id': cur_qunfa_id, 'last_qufa_time': qunfa_time,
                'update_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            })
    except KeyboardInterrupt:
        break
