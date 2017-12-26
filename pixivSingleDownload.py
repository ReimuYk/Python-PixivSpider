import urllib.request,urllib.error
import re,os
import time
from multiprocessing import Process,Queue
import requests

workplace="./img/keta/"
######################
s = requests.Session()
class pixiv:
    def __init__(self):  
        self.baseUrl = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"  
        self.LoginUrl = "https://accounts.pixiv.net/api/login?lang=zh"  
        self.firstPageUrl = 'http://www.pixiv.net/member_illust.php?id=7210261&type=all'  
        self.loginHeader = {    
        'Host': "accounts.pixiv.net",    
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",    
        'Referer': "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",  
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",  
        'Connection': "keep-alive"  
        }    
        self.return_to = "http://www.pixiv.net/"    
        self.pixiv_id = '513639514@qq.com',  
        self.password = 'chinuomi'  
        self.postKey = []  
  
    #获取此次session的post_key  
    def getPostKey(self):  
        loginHtml = s.get(self.baseUrl)  
        pattern = re.compile('<input type="hidden".*?value="(.*?)">', re.S)  
        result = re.search(pattern, loginHtml.text)  
        self.postKey = result.group(1)  
  
    #获取登陆后的页面  
    def getPageAfterLogin(self,url):  
        loginData = {"pixiv_id": self.pixiv_id, "password": self.password, 'post_key': self.postKey, 'return_to': self.return_to}   
        s.post(self.LoginUrl, data = loginData, headers = self.loginHeader)  
        targetHtml = s.get(url)  
        return targetHtml.text
######################

p=pixiv()

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    html = p.getPageAfterLogin(url)
    return html

def getReferer(url):
    reference = "http://www.pixiv.net/member_illust.php?mode=mange_big&illust_id="
    reg = r'.+/(\d+)_p0'
    return reference + re.findall(reg,url)[0] + "&page=0"

def savePic(u,filename):
    Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection":"keep-alive",
               "Referer":""}
    u=u.replace(r'c/600x600/img-master',r'img-original')
    u=u.replace(r'_master1200','')
    #print(u)
    Headers['Referer']=getReferer(u)
    
    req=urllib.request.Request(u,None,Headers)
    res=urllib.request.urlopen(req,timeout=1)
    
    rstream=res.read()
    res.close()
    
    with open(workplace+filename+".jpg",'wb') as f:
        f.write(rstream)

def intoHtml(url):
    html = getHtml(url)
    #print(html)
    reg = r'.+src="(https://i.pximg.net/c/.+_p0_master1200.jpg)'
    newUrl = re.findall(reg,html)[0]
    #print("new:"+newUrl)
    return newUrl

def getSingleID(ID):
    url=r"https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+ID 
    try:
        url=intoHtml(url)
        print(ID+" download...",end='\t')
        savePic(url,ID)
        print(ID+" done.")
    except Exception as e:
        print(ID,end=":")
        print(e)

def pixivFile(filename):
    f=open(filename,'r',encoding='utf-8')
    h=f.read()
    fileR=r'.+?/(\d+)_p\d+_master1200.jpg'
    IDlist=re.findall(fileR,h)
    return IDlist


    

def MAIN():
    filehead="./html/k"
    filetail=".html"
    for i in range(1,3):
        print("page "+str(i))
        midstr=str(i)
        if len(midstr)<2:
            midstr='0'+midstr
        file=filehead+midstr+filetail
        IDlist=pixivFile(file)
        print(IDlist)
        for ID in IDlist:
            try:
                getSingleID(ID)
            except:
                pass

#MAIN()


