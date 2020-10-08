import time
import datetime
import page
import photo
import pixivhelper
import emailsender
import threading
global photoList 
global event
photoList = []
def getDateAgo(date):
    threedayago = datetime.datetime.now() - datetime.timedelta(days=3)
    #timestamp = int(time.mktime(threedayago.timetuple()))
    
    date = threedayago.strftime("%Y%m%d")
    print(date)
    return date
def getSecondToTime(wanderHour,wanderMin):
    timestruct = datetime.datetime.now()
    tomorrowstruct = timestruct + datetime.timedelta(days=1)
    timeToday = timestruct.replace(hour=wanderHour,minute=wanderMin)
    timeTomorrow = tomorrowstruct.replace(hour=wanderHour,minute=wanderMin)
    #print(timeToday)
    #print(timeTomorrow)
    now = time.time()
    today =timeToday.timestamp()
    tomorrow = timeTomorrow.timestamp()
    #print("now is "+str(now)+" today is "+str(today)+" delta is "+str(today-now))
    if (today - now) >0:
        print("next time is today "+str(today-now)+"s ago")
        return today - now
    else:
        print("next time is tomorrow, "+str(tomorrow-now)+"s ago")
        return tomorrow - now
def getRankTop(date,ctrl):
    global event
    allID = pixivhelper.getRank(date,"daily","illust")
    print(allID)
    if len(allID) < 1:
        return ;
    
    id = allID[0]
    mpage = page.getPageByID(id)
    for id in allID:
        if (not mpage == None) and (mpage.type == "Single") : # page type may not support now, check it
            print("*********************photo fit**************************")
            if not id in photoList:
                photoList.append(id)
                break #check same photo
        print("------------------------photo not fit get next one**************************")
        mpage = page.getPageByID(id)
    
    photo = mpage.getFirstPhoto()
    if  photo:
        photoDir = "D:\\pixiv_photo\\"+date
        if event.isSet():
            return ;
        photo.printi(photoDir)
        if not event.isSet():
            event.set()
            emailsender.sendPhotoMail(photoDir+"\\"+photo.getFileName(),id = photo.getFileName())
    else:
        print("there is not photo")
    
    
# 逻辑 ：
# 1 每5min起一个thread 去爬图
# 2 一段时间后去看下结果是否发出来
# 3 
    
def dailyPhoto():
    global event
    while True:
        event = threading.Event()
        event.clear()
        count = 0
        while not event.isSet():
            count = count + 1
            date = getDateAgo(3)
            ctrl = 500
            threading.Thread(target=getRankTop,args=(date,ctrl,)).start()#there need a ','
            time.sleep(30)#sleep here 30seconds
        print("photo send success,photo list:",photoList)
        #time.sleep(5)#start at am 5:50 clock
        
        time.sleep(getSecondToTime(5,50))#start at am 5:50 clock
        print("photo list:",photoList)
    #TODO:
    # made an new thread,to run getRankTop,and then wait one day    


def main():
    dailyPhoto()
    
if __name__ == "__main__":
    #getSecondToTime(1,1)
    main()