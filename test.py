import urllib.request,urllib.error
import re,os
import time
from multiprocessing import Process,Queue



def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    return html

url=r'https://www.pixiv.net/member_illust.php?id=4920496&p=2'
#h=getHtml(url)

Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection":"keep-alive",
               "Referer":"https://www.pixiv.net/member_illust.php?id=4920496&type=all&p=2"}


dic={'id':'4920496',
    'type':'all',
     'p':'2'}

data=urllib.parse.urlencode(dic)
data=bytes(data.encode('utf-8'))

req=urllib.request.Request(url)
res=urllib.request.urlopen(req)
h=res.read().decode('utf-8')

rg=r'id=(\d+)'
idlist=re.findall(rg,h)[3:]
