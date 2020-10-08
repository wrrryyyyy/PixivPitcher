import pixivhelper
import os
class Photo(object):
    
    def __init__(self,type,pageUrl,photoUrl,photoName = "def",index = -1,page = None):
        self.type = type
        self.page = page
        self.photoUrl = photoUrl
        self.pageUrl = pageUrl
        self.photoName = photoName
        self.index = index
    # savePath not need fileName,and not need end with \
    def getTypeDir(self):
        return ""
    def printi(self,savePath):#last bit not need is \\
        str = self.photoName
        # if not (savePath[-1] == '\\' OR savePath[-1] == '/'):
        #     str = "\\"+str
        if self.index !=-1:
            str = str + self.index
        str = str + "."+self.type
        typeDir = self.getTypeDir()
        if not typeDir == "":
            str = typeDir + "\\" + str
        if savePath and (not savePath == ""):
            if not (os.path.exists(savePath)):
                os.mkdir(savePath)
        pixivhelper.httpSave(savePath+"\\"+str,self.photoUrl,self.pageUrl)
    def getFileName(self):
        return self.photoName+"."+self.type

class DynamicPhoto(Photo):
    pass
    # def __init__(self,type = "gif",pageUrl,photoUrl,page =None):
    #     super(DynamicPhoto,self).__init__(type,pageUrl,photoUrl,page)
    # def printi(self,fullPath):
    # #TODO : pixiv gif save as zip file,we need unzip it ,and then transform all 
    #       png in zip to gif file.
   

class StaticPhoto(Photo):
    pass
def getPhotoByUrl(page,url,index = -1):
        if page.type == "Single" or page.type == "Multiple" or page.type == "Manga":
            tail = pixivhelper.getTail(url)
            photo = StaticPhoto(tail,page.pageUrl,url,page.ID,index,page)
            print("get single photo"+photo.getFileName())
        if page.type == "GIF":
            photo = DynamicPhoto(page.type,page.pageUrl,url,page.ID,index,page)
        return photo