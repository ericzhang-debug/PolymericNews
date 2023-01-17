from BingUtils import getBingDescription,getBingImage,getFakerHeaders,insert,getBingVerticalImage
import datetime,requests,os
from Util import printlog

def run():
    description=getBingDescription()
    printlog("Start to download...")
    filename=str(datetime.date.today())+"/Bing每日一图"

    base='Downloads/'+filename+"/"

    location=base+description['title']+".jpg"
    url=str(getBingImage())
    url_phone=str(getBingVerticalImage())

    printlog("桌面图片请求URL: "+url)
    printlog("移动端图片请求URL: "+url_phone)

    response = requests.get(url, stream=True)
    response_phone = requests.get(url_phone, stream=True)

    if(not os.path.exists("Downloads")):
        os.mkdir("Downloads")

    if(not os.path.exists(os.path.abspath('.')+'/Downloads/'+str(datetime.date.today()))):
        os.mkdir(os.path.abspath('.')+'/Downloads/'+str(datetime.date.today()))

    if(not os.path.exists(os.path.abspath('.')+'/Downloads/'+filename)):
        os.mkdir(os.path.abspath('.')+'/Downloads/'+filename)

    # desktop photo
    with open(os.path.abspath('.')+'/Downloads/'+filename+"/"+description['title']+".jpg",'wb') as file:
        for i in response:
            file.write(i)
        file.close()
        printlog("Desktop Bing Image Download Successfully!")

    # Mobile photo
    with open(os.path.abspath('.')+'/Downloads/'+filename+"/"+"适配手机"+description['title']+".jpg",'wb') as file:
        for i in response_phone:
            file.write(i)
        file.close()
        printlog("Mobile Bing Image Download Successfully! ")

    des=os.path.abspath('.')+'/Downloads/'+filename+"/"+"描述.txt"

    with open(des,'w+') as file:
        file.write("题目："+description['headline'])
        file.write('\n')
        file.write('\n')
        file.write("标题："+description['title'])
        file.write('\n')
        file.write('\n')
        file.write("描述："+description['description'])
        file.write('\n')
        file.write('\n')
        file.write("图片信息："+description['main_text'])
    # try:
    #     insert(description['headline'],description['title'],description['description'],description['main_text'],datetime.date.today(),url,url_phone)
    # except Exception:
    #     printlog("SQLite数据库有误，无法写入数据库")