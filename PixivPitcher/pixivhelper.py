import requests
import re
import emailsender
from urllib.request import urlretrieve
global defCookies 
defCookies = "123"
defHomePath = "https://www.pixiv.net/"
defArtworkPath = "https://www.pixiv.net/artworks/83681981"
defPhotoPath = "https://i.pximg.net/c/48x48/img-master/img/2020/08/15/00/00/24/83681981_p0_square1200.jpg"
inited = False
def getHandler(addHeader = {}): 
    defHeader = {
        "Accept": "application/json, text/javascript, */*; q=0.01" ,
        "Accept-Encoding": "gzip, deflate" , 
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3" ,
        "Cache-Control": "max-age=0",
        "Host": "www.pixiv.net" ,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" ,
        "Referer":"" ,
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": defCookies ,
    }
    if not (addHeader == None):
        for str in addHeader.keys():
            defHeader[str] = addHeader[str]
   # print(defCookies)
    return defHeader

def init():
    global defCookies 
    global inited 
    cookieFile = open("cookies.txt","r+",encoding="utf-8")
    str = cookieFile.read()
    defCookies = str
    #print(defCookies)
    req = requests.get(defArtworkPath,verify=False,headers=getHandler())

    if not checkCookiesUseable(req.text) : 
        print("error: init faile, cookie may unuseable ")
    else:
        print("init success")
        inited = True
    return inited

def saveToFile(fileName,str):
    target = open(fileName,"w",encoding= "utf-8")
    target.write(str)

def checkCookiesUseable(str):
    checkStr = "「こんな感じ～？」" #use this string to check cookies is usable
    if checkStr in str:
        return True
    return False

def tryToGet(url,handler = {}):
    if not inited:
        if not init():
            print("error: get failed, pixiv not inited")
            return None
    req = requests.get(url,verify=False,headers=getHandler(handler))
    
    return req

def httpGet(url,handler = {}):
    req = tryToGet(url,handler)
    print("http get:",req.status_code," ",url," ")
    return req

def httpGetRef(url):
    req = tryToGet(url,{"Referer":url})
    print("http get:",req.status_code," ",url," ")
    return req


#
# if we need download an photo from pixiv
# we need set the referer to this artwork's path
# 
def httpSave(fileName,url,referer = "",host = ""):
    #req = tryToGet(url,{"Referer":referer, "Host":host})
    req = tryToGet(url,{"Referer":referer}) # use default host,request will send an warning, ignore it
    raw = req.content
    
    with open(fileName,"wb") as file:
        file.write(raw)

def getHost(url = ""):
    str1 = url.split("//",1)
    if len(str1) <=1 :
        return ""
    str2 = str1[1].split("/",1)
    if len(str2) <=1 :
        return ""
    return str2[0]
def getTail(url):
    RgetTail = "http.*/.*[.](.*)"
    return getString(url,RgetTail)
def getString(sGet,reg):

    search = re.search( r''+reg, sGet, re.M|re.I)
    if not search:
        return None
 #   print(search.group())
    return search.group(1)
def getStringRegs(sGet,regs):
    success = False
    for str in regs:
        search = re.search( r''+str, sGet, re.M|re.I)
        if search :
            return search.group(1)
    return ""
def getDailyRank():
    return []
def getID(path):
    return getString(path,".*?id=(.*)")
    

#daily 's form is like 20170103
def getRank(daily = "",mode = "",type1 = ""):
    RgetToken = "token[^:]*?\"([^:\"]*?)\""
    RgetRankTotal = "\"rank_total\":(.*?)}"
    RgetNextID = 'illust_id\":([0-9]{1,}),\"'
    path = "https://www.pixiv.net/ranking.php?"
    defMode = ["daily","weekly","monthly","rookie","male","female","daily_r18",
               "weekly_r18","monthly_r18","rookie_r18","male_r18","female_r18",]
    defType = ["illust","ugoira","manga"]
    RgetFirstPage = 'data-attr=[^-]*?data-id=.(.*?)\"'

    #check mode and date
    if mode in defMode:
        path = path + "mode=" + mode
    if type1 in defType:
        path = path + "&content=" + type1
    if not daily == "" :
        path = path + "&date=" + daily
    #send a request and get first 50 ids
    sGet = httpGet(path,{"Referer":path})
    pattern = re.compile(r""+RgetFirstPage,re.M)  
    ID = []
    ID = ID + pattern.findall(sGet.text)
    #get second page and token, for third page
    token = getString(sGet.text,RgetToken)
    nextPath = path + "&ref=rn-h-week-3" + "&p=" + "2" + "&format=json&tt=" + token
    sGet = httpGet(nextPath)
    total = getString(sGet.text,RgetRankTotal)
    num = 50
    try:
        num = int(total)
    except expression as identifier:
        return ID
    
    pattern = re.compile(r""+RgetNextID,re.M)  
    ID = ID + pattern.findall(sGet.text)
    #get third page
    for i in range(3,int(num/50)+1):
        nextPath = path + "&ref=rn-h-week-3" + "&p=" + str(i) + "&format=json&tt=" + token
        sGet = httpGet(nextPath)
        ID = ID + pattern.findall(sGet.text)
    print("id len",len(ID))
    return ID    

#init()
#req = requests.get(defArtworkPath,verify=False,headers=getHandler())
#print(req.text)
#print(req.cookies)
#saveToFile("save.html",req.text)
#httpGet(defArtworkPath)
#httpSave("D:\\workSpace\\python_hardway\\tc050\projects\\skeleton\\PixivPitcher\\localphoto1.jpg",defPhotoPath,defArtworkPath)
#id = getRank("20200816","daily","illust")
#print(id)
