from pixivhelper import *
import photo
import re
class Page(object):
    def checkType(self,type):
        if type == "Manga" :
            return type
        if type == "Single":
            return type
        if type == "Multiple":
            return type
        if type == "GIF":
            return type
        return "Single"
    def __init__(self,pageUrl,type):
        self.pageUrl = pageUrl
        self.type = self.checkType(type)
        self.allPhotoUrl = []
        self.allPhoto = [] 
        self.photoInited = False
        self.ID = getID(self.pageUrl)
    def getFirstPhoto(self):
        if not self.photoInited :
            self.initPhotos()
        if not self.photoInited :
            print("photo not init")
            return None
        else:
            print("photo inited")
            return self.allPhoto[0]
    def getAllPhoto(self):
        if not self.photoInited :
            self.initPhotos()
        return self.allPhoto
    def printall(self):
        print("pageUrl ",self.pageUrl,"type ",self.type,"allPhoto ",str(len(self.allPhotoUrl)))
    def dealPhoto(self):
        print("deal default photo")
        
    def initPhotos(self,sGet = ""):
        self.dealPhoto()
            #TODO： add photo init
        #TODO: add Multiple and gif support
        pass

class SinglePage(Page):
    def __init__(self,pageUrl):
        super().__init__(pageUrl,type = "Single")
    def dealPhoto(self):
        print("deal singlepage photo")
        sGet =  httpGetRef(self.pageUrl).text
        RgetUrlTail = "img-original[^img]*?img[^img]*?"+self.ID+"_p.*?[.](.*?)\"" 
        RgetUrl = "img-original[^img]*?img([^img]*?"+self.ID+"_p)"
        RgetCutVV = "\\\\/"
        #print("deal single photo")
        tail = getString(sGet,RgetUrlTail)
        photoUrl = getString(sGet,RgetUrl); 
        photoUrl = re.sub(r""+RgetCutVV,"/",photoUrl)
        photoUrl = "https://i.pximg.net/img-original/img" + photoUrl +"0." + tail
        print("photoUrl:"+photoUrl)
        self.allPhotoUrl.append(photoUrl)
        mphoto = photo.getPhotoByUrl(self,photoUrl)
        if mphoto:
            self.photoInited = True
            self.allPhoto.append(mphoto) #add only one photo
        else:
            print("get photo error")
            self.printall();
                
class MultiplePage(Page):
    def __init__(self,pageUrl):
        super().__init__(pageUrl,type = "Multiple")
    def dealPhoto(self):
        print("deal Multiple photo")
            #TODO： add photo init
        #TODO: add Multiple and gif support

def getPageByID(id):
    path = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + (id)
    return getPage(path)

def getPage(path):
    #TODO: add tags support
    tags = []
    RgetTags = ""
    RgetTypes = ["illust:[^}]*?illustType\":(.*?),","illustType\":([^,]*?),\"createDate"]
    RgetPhotoNum = "[^{]*?[{][^}]*?pageCount.*?:(.*?),"
    sGet = httpGetRef(path)
    type = getStringRegs(sGet.text,RgetTypes)
    id = getID(path)
    print("type:",type ," ",path)
    photoNum = 0
    #try:
    photoNum = int(getString(sGet.text,str(id+RgetPhotoNum)))
    
    #except expression as identifier:
    #    print("error: transform photonum error")
    if photoNum == 1 and (type == "" or (not type == "2")):
        page = SinglePage(path)
        return page
    return None

#page = getPageByID("83681981")
#page.printall()
#page.initPhotos()
#httpSave("D:\\workSpace\\python_hardway\\tc050\projects\\skeleton\\PixivPitcher\\localphoto1.jpg",page.allPhotoUrl[0],page.pageUrl)
