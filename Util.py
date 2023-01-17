import datetime,os
def printlog(log):
    now=datetime.datetime.now()
    loginfo="[INFO]"+"["+now.strftime("%Y-%m-%d %H:%M:%S")+"] "+log
    print(loginfo)
    # if(not os.path.exists(os.path.abspath('.')+"\\log.txt")):
    #     os.mkdir("log.txt")
    # with open(os.path.abspath('.')+"/log.txt","a") as file:
    #     file.write(loginfo)
    #     file.write('\n')
    #     file.close()