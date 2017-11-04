import urllib.request,urllib.error
import re,os
import time
from multiprocessing import Process,Queue

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    return html

def getReferer(url):
    reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
    reg = r'.+/(\d+)_p0'
    return reference + re.findall(reg,url)[0] + "&page=0"

def savePic(u):
    Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection":"keep-alive",
               "Referer":""}
    u=u.replace(r'c/600x600/img-master',r'img-original')
    u=u.replace(r'_master1200','')
    print(u)
    Headers['Referer']=getReferer(u)
    
    req=urllib.request.Request(u,None,Headers)
    res=urllib.request.urlopen(req,timeout=1)
    
    rstream=res.read()
    res.close()
    
    with open("./img/test001.jpg",'wb') as f:
        f.write(rstream)

url=r"https://i.pximg.net/c/600x600/img-master/img/2009/07/25/07/51/04/5307115_p0_master1200.jpg"
savePic(url)
