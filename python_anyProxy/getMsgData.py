from flask import Flask, request, redirect,url_for
import html
import time
from bs4 import BeautifulSoup
from urllib.request import  urlopen
from urllib import parse
from urllib.parse import  unquote
import json
app = Flask(__name__)
import  mongo

@app.route('/getMsgData', methods=['GET', 'POST'])
def  getMsgData():
    mongodb = mongo.mongo()
    datalist = request.form.get('str')
    url = request.form.get('url')
    url = html.unescape(unquote(url))
    query = parse.urlparse(url).query
    urldict = dict([(k, v[0]) for k, v in parse.parse_qs(query).items()])
    biz = urldict['__biz']
    datalist = html.unescape(html.unescape(unquote(datalist)))
    print(datalist)
    datadict = json.loads(datalist)   #解析为python对象
    dataset = datadict['list']
    if dataset :
        for item in dataset:
            content_type = item['comm_msg_info']['type']
            if content_type == 49:
                content_url = item['app_msg_ext_info']['content_url'] #获得图文消息的链接地址
                is_multi    = item['app_msg_ext_info']['is_multi']    #是否是多图文消息
                pubtime     = item['comm_msg_info']['datetime']-28800 #图文消息发送时间
                condsql = {"content":content_url}
                num = mongodb.query('ugc_source_set', cond=condsql).count()
                if num <= 0:
                    fileid = item['app_msg_ext_info']['fileid'] #一个微信给的id
                    author = item['app_msg_ext_info']['author']
                    title  = item['app_msg_ext_info']['title']  #文章标题
                    digest = item['app_msg_ext_info']['digest'] #文章摘要
                    source_url = item['app_msg_ext_info']['source_url'] #阅读原文的链接
                    cover = item['app_msg_ext_info']['cover']#封面图片
                    is_top = 1 #标记一下是头条内容
                    sql = {"content":content_url, "pubtime_utc":pubtime,"title":title, "desc":digest, "source":source_url,"image":cover,"author":author, "type":1, "data":{"is_top":is_top,"is_multi":is_multi,"fileid":fileid,"biz":biz}}
                    mongodb.insert('ugc_source_set',sql)
                if is_multi == 1:
                    for  multiItem in item['app_msg_ext_info']['multi_app_msg_item_list']:
                        content_url = multiItem['content_url'] #图文消息链接地址
                         #这里再次根据$content_url判断一下数据库中是否重复以免出错
                        num = mongodb.query('ugc_source_set',{"content":content_url}).count()
                        if num <= 0:
                            title  = multiItem['title'] #文章标题
                            fileid = multiItem['fileid']    #一个微信给的id
                            digest = multiItem['digest'] #文章摘要
                            author = multiItem['author']
                            source_url = ['source_url'] # 阅读原文的链接
                            cover = multiItem['cover']
                            sql = {"content": content_url, "pubtime_utc": pubtime, "title": title, "desc": digest,
                           "source": source_url, "image": cover, "author": author, "type": 1,
                           "data": {"is_top": is_top, "is_multi": is_multi, "fileid": fileid, "biz": biz}}
                            mongodb.insert('ugc_source_set', sql)
        text = urlopen(dataset[0]['app_msg_ext_info']['content_url'])
        text = BeautifulSoup(text, 'lxml')
        titleset = text.findAll(id='post-user')
        for title in titleset:
                # print("微信公众号名称%s"%title.get_text())
                condsql = {'biz': biz, 'title': title.get_text()}
                num = mongodb.query('ugc_zone', condsql).count()
                createtime = time.time() - 28800

                if num == 0:
                    condsql = {'biz': biz, 'title': title.get_text(), 'updatetime':createtime}
                    mongodb.insert('ugc_zone', condsql)
                else:
                    updateSql = {'updatetime':createtime}
                    mongodb.update('ugc_zone', condsql, updateSql)

    return "hello"


if __name__ == '__main__':
    app.run()
