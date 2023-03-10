from faker import Faker
import requests
import parsel
import json
import re,logging
import sqlite3
import datetime
import os
from time import strftime,gmtime
from Util import printlog

TYPES=["PHONE","DESKTOP","RANDOM"]
url = 'https://cn.bing.com'

def getFakerHeaders(TYPE):
    fake = Faker()
    if str(TYPE).upper()=="PHONE":
        return 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; hsb-DE) AppleWebKit/531.21.4 (KHTML, like Gecko) Version/3.0.5 Mobile/8B116 Safari/6531.21.4'
    if str(TYPE).upper() == "DESKTOP":
        return 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_5 rv:5.0; the-NP) AppleWebKit/534.2.5 (KHTML, like Gecko) Version/5.0.5 Safari/534.2.5'
    if str(TYPE).upper() == "RANDOM":
        return fake.user_agent()


def getBingImage():
    headers= {"user-agent": getFakerHeaders("DESKTOP")}
    # logging.info("本次Headers:"+headers["user-agent"])
    respond=requests.get(url=url,headers=headers)
    respond.encoding = respond.apparent_encoding
    selector = parsel.Selector(respond.text, base_url=url)
    url1=str(selector.css('#preloadBg::attr(href)').extract_first())
    url1=confirmURL(url1)
    return url1

def getBingVerticalImage():
    headers= {"user-agent": getFakerHeaders("PHONE")}
    respond=requests.get(url=url,headers=headers)
    respond.encoding = respond.apparent_encoding
    selector = parsel.Selector(respond.text, base_url=url)
    # return selector.css('#preloadBg::attr(href)').extract_first()
    url1=str(selector.css('#preloadBg::attr(href)').extract_first())
    url1=confirmURL(url1)
    return url1

def getBingDescription():
    headers = {
        'user-agent':getFakerHeaders('DESKTOP')
    }
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding

    # res1 = requests.get(r"https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN", headers=headers)
    # res1.encoding = res1.apparent_encoding
    # data1=json.loads(res1.content)
    # out_copyright=data1['images'][0]["copyright"]
    # out_copyright=out_copyright.encode('utf-8')

    ret = re.search("var _model =(\{.*?\});", res.text)
    if not ret:
        return
    data = json.loads(ret.group(1))
    image_content = data['MediaContents'][0]['ImageContent']
    return {
        'headline': image_content['Headline'],
        'title': image_content['Title'],
        'description': image_content['Description'],
      #  'image_url': image_content['Image']['Url'],
        'main_text': image_content['QuickFact']['MainText'],
        # 'copyright': out_copyright
    }

def insert(headline,title,description,main_text,add_data,url_desktop,url_mobile):
    name='IMAGEDB.sqlite'
    conn = sqlite3.connect(name)
    c = conn.cursor()
    sql="insert into image(id,headline,title,description,main_text,add_date,url_desktop,url_mobile) values(null,'%s','%s','%s','%s','%s','%s','%s')"%(headline,title,description,main_text,add_data,url_desktop,url_mobile)
    printlog("SQL ===>"+sql)
    c.execute(sql)
    conn.commit()
    printlog("SQLite数据库写入成功")
    conn.close()

def confirmURL(url):
    url_head=str(url)
    result=""
    if(url_head[0:6]=="/th?id"):
        result="https://s.cn.bing.net"+url_head
        return result
    else:
        return str(url)
