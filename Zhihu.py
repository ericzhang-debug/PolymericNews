import datetime
import requests
import time
import os
import pandas as pd #Need openpyxl
from Util import printlog

def run():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }

    if(not os.path.exists("Downloads")):
        os.mkdir("Downloads")

    if(not os.path.exists(os.path.abspath('.')+'/Downloads/'+str(datetime.date.today()))):
        os.mkdir(os.path.abspath('.')+'/Downloads/'+str(datetime.date.today()))

    if(not os.path.exists(os.path.abspath('.')+'/Downloads/'+str(datetime.date.today())+'/Zhihu')):
        os.mkdir(os.path.abspath('.')+'/Downloads/'+str(datetime.date.today())+'/Zhihu')
    
    now_time = datetime.datetime.now()
    year = now_time.year
    month = now_time.month
    day = now_time.day
    hour = now_time.hour
    sess = requests.Session()
    res = sess.get(url, headers=headers)
    data = res.json()["data"]
    #print(data)
    hot_list = []

    id=[]
    title=[]
    link=[]
    create_time=[]
    itype=[]
    answer_count=[]
    follower_count=[]


    for item in data:
        item_id = item["target"]["id"]
        item_title = item["target"]["title"]

        id.append(item_id)
        title.append(item_title)
        link.append(item["target"]["url"])
        create_time.append((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item["target"]["created"]))))
        itype.append(str(item["target"]["type"]).capitalize())
        answer_count.append(item["target"]["answer_count"])
        follower_count.append(item["target"]["follower_count"])
        

       # hot_list.append("{}: {}".format(item_id, item_title))
        hot_list.append("[{}]({}): {}".format((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item["target"]["created"]))),item_id, item_title))

    output = "\n".join(hot_list)
    printlog("知乎热搜数据获取成功")
    file_path=os.path.abspath('.')+'/Downloads/'+str(datetime.date.today())+'/Zhihu/'
    file=file_path+"{}-{}-{}_{}时简略数据.txt".format(year, month, day, hour)
    with open(file, mode="w") as f:
        f.write(output)
    excel_file=file_path+"{}时完整数据.xlsx".format(hour)
    df = pd.DataFrame(
	{
		'ID': id,
		'标题': title,
		'创建时间': create_time,
		'类型': itype,
        '回复数': answer_count,
        '关注数': follower_count,
		'API地址': link
	}
    )
    df.to_excel(excel_file, index=False)


'''
知乎API：
当前热搜
URL: https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true
返回json

根据问题ID获取API
https://api.zhihu.com/questions/<id>

'''
'''
https://zhuanlan.zhihu.com/p/463667802
'''