import blblhelper
import time
import emailsender
import threading
#import bs4
global fanInited
configFile = "blbl.cvs"
fanInited = 0
global blblConfigs 
blblConfigs= {"userid":"","fan_check_delay":"1","mail_notify":"True","mail_notify_delta":""}
inited= 0
def setConfig(line):
    global fanInited 
    global blblConfigs
    configKey = blblConfigs.keys()
    allValue = line.split(",")# this way may have an /n include in value
    if len(allValue) >=2:
        key = allValue[0]
        value = allValue[1]
        if key in configKey:
            blblConfigs[key] = value

def initFanCheck():
    global fanInited
    if fanInited == 0:
        configs = open(configFile)
        if configs.readable():
            lines = configs.readlines()
            for line in lines:
                setConfig(line)
            configs.close()
        fanInited = 1
    
def fanNotify(fans,detal):
    message = ""
    if detal > 0 :
        message = f"刚刚又有{detal}个小伙伴关注了你，现在总共{fans}个粉丝啦！"
    else :
        detal1 = detal * (-1)
        message = f"刚刚有{detal1}个粉丝取关，现在只有{fans}个粉丝了，快反思下平日的所作所为"
    emailsender.sendTextMail("粉丝数更新啦",message)
    pass
def notifyDriver(fans):
    pass
def autoFanCheck(id,sendMail = False,sec = 1.0, delta = 1):
    fans = "0"
    fans = int(blblhelper.fansCheck(id))
    while True:
        newFans = int(blblhelper.fansCheck(id))
        if not fans == newFans:
            notifyDriver(newFans)
            if sendMail :
                nowDelta = newFans - fans
                posDelta = nowDelta
                if posDelta < 0 :
                    posDelta = posDelta * (-1)
                if(posDelta >= delta): #now need notify
                    fans = newFans
                    fanNotify(fans,nowDelta)
                else :
                    print("fans freash,but not need notify now ,",time.strftime("%m/%d %H:%M"))
            pass
        time.sleep(sec)
        

def autoFanCheckThread():
    autoFanCheck(blblConfigs["userid"],bool(blblConfigs["mail_notify"]),sec = float(blblConfigs["fan_check_delay"]),delta = int(blblConfigs["mail_notify_delta"]))

def main():
    if fanInited == 0 :
        initFanCheck()
        print(blblConfigs)
    if fanInited == 1 :
        thread = threading.Thread(target=autoFanCheckThread)
        thread.start()
        if thread.is_alive():
            time.sleep(360)
        else :
            print("blbl thread dead,reinit")
            thread = threading.Thread(target=autoFanCheckThread)
            thread.start()
        
        

if __name__ == "__main__":
    main()  
