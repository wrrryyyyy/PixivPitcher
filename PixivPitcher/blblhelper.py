import requests
import pixivhelper
blblHandler = {
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"cache-control": "max-age=0",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59",
}
fanHandler = {
"accept": "application/json, text/plain, */*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"origin": "https://space.bilibili.com",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-site",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59",
}

myuserpage = "https://space.bilibili.com/{}"
myfunapi = "https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp"
cookieapi = "https://api.bilibili.com/x/web-show/res/locs?pf=0"
def getCookie(req):
    cookies = req.cookies.items()
    cookie = ''
    for name, value in cookies:
        cookie += '{0}={1};'.format(name, value)
    return cookie
def webget(url,handler = {},addHandler = {}):
    getHandler = handler.copy()
    for key in addHandler.keys():
        getHandler[key] = addHandler[key]
    req = requests.get(url,verify=False,headers =getHandler)
    print("http get:",req.status_code," ",url," ")
    
    return req
#print(req.text)
def fansCheck(id):
    userpage = myuserpage.format(id)
    funapi = myfunapi.format(id)
    RgetFollow = "follower.*?([0-9].*?)[^0-9]"
    req = webget(userpage,blblHandler)
    #print(req.text)
    req = webget(cookieapi,fanHandler)
    #print(getCookie(req))
    cookie = getCookie(req)
    req = webget(funapi,fanHandler,{"referer": userpage,"cookie": cookie})
    print(req.text)
    fans = pixivhelper.getString(req.text,RgetFollow)
    
    return fans

if __name__ == "__main__":
    get = fansCheck("11941487")
    print(get)
