import urllib.request,urllib.error
import re,os
import time
import codecs
from multiprocessing import Process,Queue

jpgReg=r'https://i.pximg.net/img.+?master1200.jpg'

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    return html

def getReferer(url):
    reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
    reg = r'.+/(\d+)_p'
    regNum=r'.+/\d+_p(\d+)'
    return reference + re.findall(reg,url)[0] + "&page=" + re.findall(regNum,url)[0]

def savePic(u,dirname,i):
    isexist=os.path.exists("./img/"+dirname+'/'+dirname+'_'+str(i)+".jpg")
    if isexist:
        return
    Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection":"keep-alive",
               "Referer":""}
    #u=u.replace(r'img-master',r'img-original')
    #u=u.replace(r'_master1200','')
    #print(u)
    Headers['Referer']=getReferer(u)
    
    req=urllib.request.Request(u,None,Headers)
    res=urllib.request.urlopen(req,timeout=5)
    rstream=res.read()
    res.close()

    try:
        os.mkdir("./img/"+dirname)
    except:
        pass
    try:
        file=open("./img/"+dirname+'/'+dirname+'_'+str(i)+".jpg",'wb')
        file.write(rstream)
    except:
        pass
        
    

def pixivGet(ID):
    urlHead=r'https://www.pixiv.net/member_illust.php?mode=manga&illust_id='
    url=urlHead+ID
    h=getHtml(url)
    ulist=re.findall(jpgReg,h)
    for i in range(len(ulist)):
        savePic(ulist[i],ID,i)

def pixivList(idlist):
    for ID in idlist:
        try:
            print(ID+" download...",end='\t')
            pixivGet(ID)
            print(ID+" done.")
        except Exception as e:
            print(ID,end=":")
            print(e)

def pixivFile(filename):
    f=open(filename,'r',encoding='utf-8')
    h=f.read()
    fileR=r'.+?/(\d+)_p\d+_master1200.jpg'
    IDlist=re.findall(fileR,h)
    #print(ulist)
    for ID in IDlist:
        try:
            print(ID+" download...",end='\t')
            pixivGet(ID)
            print(ID+" done.")
        except Exception as e:
            print(ID,end=":")
            print(e)
            #print(ID+" is not a set of pics")
    
Main_url=r'https://www.pixiv.net/member_illust.php?id=4920496&type=all'


'''
while True:
    fullUrl=Main_url
    if not page==1:
        fullUrl=fullUrl+r'&p='+str(page)
    print(fullUrl)
    fullUrl=r'https://www.pixiv.net/member_illust.php?id=4920496&type=all&p=2'
    try:
        ht=getHtml(fullUrl)
    except:
        print("Have Done!")
        break
    rg=r'id=(\d+)'
    idlist=re.findall(rg,ht)[3:]
    for item in idlist:
        print(item,end='')
        try:
            pixivGet(item)
            print("Done")
        except:
            print("Item Passed")
    page+=1

for i in range(30,32):
    numstr=str(i)
    print("page "+numstr)
    if len(numstr)<2:
        numstr='0'+numstr
    filepath="./html/page"+numstr+".html"
    try:
        pixivFile(filepath)
    except:
        print("Error in range "+str(i))'''

def reHistory(filename):
    file=open("./history/"+filename,'r')
    linelist=file.readlines()
    IDlist=[]
    for item in linelist:
        if "timed out" in item:
            IDlist.append(item[0:8])
    for ID in IDlist:
        try:
            print(ID+" download...",end='\t')
            pixivGet(ID)
            print(ID+" done.")
        except Exception as e:
            print(ID,end=":")
            print(e)










