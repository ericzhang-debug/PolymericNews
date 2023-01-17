import re
import time
import requests
# url编码和解码
from urllib import parse

###网址
url="https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
###模拟浏览器，这个请求头windows下都能用
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

###获取html页面
html=etree.HTML(requests.get(url,headers=header).text)
def OneHot(i):
    findhot = '#pl_top_realtimehot > table > tbody > tr:nth-child('+str(i)+') > td.td-02 > a'
    hot = r.html.find(str(findhot),first = True)
    if(i<=10):
        print(str(i-1)+'   '+hot.text)
    else:
        print(str(i-1)+'  '+hot.text)
        