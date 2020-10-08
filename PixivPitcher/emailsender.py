import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
global mailConfig 
global inited 
mailConfig= {"smtp_host":"","from_addr":"","send_addr":"","password":""}
inited= 0
def setConfig(line):
    global inited 
    global mailConfig
    configKey = mailConfig.keys()
    allValue = line.split(",")# this way may have an /n include in value
    if len(allValue) >=2:
        key = allValue[0]
        value = allValue[1]
        if key in configKey:
            mailConfig[key] = value
def checkConfig():
    global mailConfig
    values = mailConfig.values()
    for val in values:
        if val == "": #any one not init,return false
            return False
    return True #all inited,return true
def init_mail():
    global inited
    if inited == 0:
        configs = open("configs.cvs")
        if configs.readable():
            lines = configs.readlines()
            for line in lines:
                setConfig(line)
            configs.close()

        if checkConfig():
            inited = 1
        else :
            inited = -1
    print(mailConfig)
    print("init done:",inited)
    if inited == -1:
        return False
    else :
        return True

def sendPhotoMail(photo,id = ""):
    if id == "":
        sendMail("今天也要加油鸭(๑•̀ㅂ•́)و✧","<img src=\"cid:image1\"/></br><ul><li><font size=\"2\">今天也要加油！</font><br>",photo)
    else:
        sendMail("今天也要加油鸭(๑•̀ㅂ•́)و✧","<img src=\"cid:image1\"/></br><ul><li><font size=\"2\">今天也要加油！</font><br><font size=\"1\">"+id+":</font></li></ul><br>",photo)
    
def sendTextMail(subject,body):
    init_mail() #what every inited or not ,init it
    sender = mailConfig["from_addr"] 
    receivers = mailConfig["send_addr"]
    message = MIMEText(body,_subtype="plain",_charset="utf-8")
    message['From'] = sender #if we use html form, we should not use alias
    message['To'] = receivers
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mailConfig["smtp_host"],25)#163 qq  default host is 25
        smtpObj.login(mailConfig['from_addr'],mailConfig['password'])
        smtpObj.sendmail(sender,receivers,message.as_string())
        print ("发件成功！")
        smtpObj.quit
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
    
def sendMail(subject,body,photo):
    init_mail() #what every inited or not ,init it
    sender = mailConfig["from_addr"] 
    receivers = mailConfig["send_addr"]
    message = MIMEMultipart()#"alternative") #defalut is Plain
    #message['From'] = sender #if we use html form, we should not use alias
    #message['From'] = "亲切的邮件妖精" #if we use html form, we should not use alias
    message['From'] = "綺麗正しきメイル妖精" #if we use html form, we should not use alias
    message['To'] = receivers
    message['Subject'] = Header(subject, 'utf-8')
    fp = open(photo,"rb")
    img = MIMEImage(fp.read())
    img.add_header("Content-ID","<image1>")
    fp.close()
    fp = open(photo,"rb")
    img1 = MIMEImage(fp.read())
    fp.close()
    img1.add_header('Content-Disposition', 'attachment', filename='image1.jpg')
    img1.add_header("Content-ID","<image2>")
    message.attach(img)
    #message.attach(img1)
    txt = MIMEText(body,_subtype="html",_charset="utf-8")
    message.attach(txt)
    plain = MIMEText("今天也要加油！",_subtype="plain",_charset="utf-8")
    message.attach(plain)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mailConfig["smtp_host"],25)#163 qq  default host is 25
        smtpObj.login(mailConfig['from_addr'],mailConfig['password'])
        smtpObj.sendmail(sender,receivers,message.as_string())
        print ("发件成功！")
        smtpObj.quit
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mailConfig["smtp_host"],25)#163 qq  default host is 25
        smtpObj.login(mailConfig['from_addr'],mailConfig['password'])
        smtpObj.sendmail(sender,receivers,message.as_string())
        #print ("发件成功！")
        smtpObj.quit
    
if __name__ == "__main__":
    #sendMail("今天也要加油鸭(๑•̀ㅂ•́)و✧","<img src=\"cid:image1\"/></br><ul><li><font size=\"2\">今天也要加油！</font></li></ul><br>","localphoto.jpg")
    sendTextMail("粉丝数提醒","粉丝数变化啦 ！")
    #dzgeguqonfmbhgch
    #kocrhpzrusmachca

 
 