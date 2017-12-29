import urllib.request,urllib.error
import re,os
import time
import codecs
import requests
from copy import *

workplace = r"./img/"
successNum = 0

s = requests.Session()

# init func
def getHtml(url):
    html = s.get(url).text
    return html

# init func
def getReferer(url):
    reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
    reg = r'.+/(\d+)_p'
    regNum=r'.+/\d+_p(\d+)'
    return reference + re.findall(reg,url)[0] + "&page=" + re.findall(regNum,url)[0]

# init func
def intoHtml(url):
    html = getHtml(url)
    reg = r'.+src="(https://i.pximg.net/img-original/img/.+?_p0.+?)"'
    newUrl = re.findall(reg,html)[0]
    return newUrl

checkButton = True
def checkFileExist(path):
    return os.path.exists(path) and checkButton
        
def savePic(url,path,PID,id_type,i):
    filename = deepcopy(PID)
    Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection":"keep-alive",
               "Referer":""}
    if id_type=='single':
        Headers['Referer']=getReferer(url)
        rstream = s.get(url,headers=Headers).content
        filename = filename + '.' + url[-3:]
        ret = 'single-' + url[-3:]
    if id_type=='set':
        Headers['Referer']=getReferer(url)
        filename = filename + '_' + str(i) + '.jpg'
        rstream = s.get(url, headers=Headers).content
        ret = 'set'
    filepath = path + filename
    with open(filepath, 'wb') as f:
        f.write(rstream)
    return ret

def setDownload(PID,username):
    urlHead=r'https://www.pixiv.net/member_illust.php?mode=manga&illust_id='
    url=urlHead+PID
    h=getHtml(url)
    jpgReg=r'https://i.pximg.net/img.+?master1200.jpg'
    ulist=re.findall(jpgReg,h)
    if len(ulist)==0:
        return False
    workpath = workplace + username + r'/' + PID + r'/'
    try:
        os.mkdir(workpath)
    except:
        pass
    for i in range(len(ulist)):
        if not checkFileExist(workpath+PID+'_'+str(i)+'.jpg'):
            savePic(ulist[i],workpath,PID,'set',i)
    return True

def singleDownload(PID,username):
    url = r"https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+PID
    url = intoHtml(url)
    workpath = workplace + username + r'/'
    res = 'exist'
    if not (checkFileExist(workpath+PID+'.jpg')or checkFileExist(workpath+PID+'.png')):
        res = savePic(url,workpath,PID,'single',0)
    return res

def getByPID(PID,username):
    print(username,PID+' download...',end='\t')

    stat = setDownload(PID,username)
    if stat:
        return 'set'
    stat = singleDownload(PID,username)
    return stat


def pixivLogin():
    # init parameter
    baseUrl = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"  
    LoginUrl = "https://accounts.pixiv.net/api/login?lang=zh"  
    firstPageUrl = 'http://www.pixiv.net/member_illust.php?id=7210261&type=all'  
    loginHeader = {    
    'Host': "accounts.pixiv.net",    
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",    
    'Referer': "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",  
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",  
    'Connection': "keep-alive"  
    }    
    return_to = "http://www.pixiv.net/"    
    pixiv_id = '513639514@qq.com'
    password = 'chinuomi'  
    postKey = []
    # get postKey
    loginHtml = s.get(baseUrl)  
    pattern = re.compile('<input type="hidden".*?value="(.*?)">', re.S)  
    result = re.search(pattern, loginHtml.text)  
    postKey = result.group(1)
    # login
    loginData = {"pixiv_id": pixiv_id, "password": password, 'post_key': postKey, 'return_to': return_to}   
    s.post(LoginUrl, data = loginData, headers = loginHeader)

user_dict={}#dictionary of {UID : username}
user_ignore=['11','4920496']
def getUserDict():
    url=r'https://www.pixiv.net/bookmark.php?type=user'
    f_html = s.get(url).text
    r1 = r'data-user_id="(\d+)"'
    UIDlist = re.findall(r1,f_html)
    UIDlist = UIDlist[4:]
    r2 = r'data-user_name="(.+?)"'
    UNlist = re.findall(r2,f_html)
    for i in range(len(UIDlist)):
        user_dict[UIDlist[i]] = UNlist[i]

def getUserPIDs(UID):
    urlhead = r'https://www.pixiv.net/member_illust.php?id='+UID+'&type=all&p='
    res = []
    page_num = 1
    while True:
        try:
            url = urlhead + str(page_num)
            pageHtml = getHtml(url)
            pageR = r'.+?/(\d+)_p\d+_master1200.jpg'
            PIDlist = re.findall(pageR, pageHtml)
            res = res + PIDlist
            if len(PIDlist)==0:
                break
            page_num += 1
        except:
            pass
    return res

def getUserPics(UID,username):
    workpath = workplace + username + r'/'
    try:
        os.mkdir(workpath)
    except:
        pass
    PIDlist = getUserPIDs(UID)
    for PID in PIDlist:
        try:
            stat = getByPID(PID,username)
            print('type:',stat)
        except Exception as e:
            f = open(r"./history/report.txt",'a+')
            f.write(PID+'\t'+str(e)+'\n')
            f.close()
            print('type:error ',e)
        
def interestDownload():
    pixivLogin()
    getUserDict()
    for k,v in user_dict.items():
        print('\n',k,v)
        if not k in user_ignore:
            getUserPics(k,v)
    
def test():
    global workplace
    workplace = r'./test/'
    getUserPics('4425133','ちくわぶ汰')
    

def test1():
    global workplace
    workplace = r'./test/'
    print(getByPID('65995669','none'))#R18 set 2
    print(getByPID('66046561','none'))#normal single jpg
    print(getByPID('66144478','none'))#R18 single jpg
    print(getByPID('25930360','none'))#normal set 3
    print(getByPID('7823236','none'))#normal single png
    print(getByPID('62742920','none'))#normal single png
    

interestDownload()
