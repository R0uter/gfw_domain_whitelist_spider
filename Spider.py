import Reviewer
import urllib3
import certifi
import re
import subprocess
import shlex
import codecs
import chardet



#爬虫类
class Spider:
    __domainList = []
    __whiteList = []

    def __init__(self,ioMethod):
        self.__io = ioMethod
        self.__reviewer = Reviewer.Reviewer(self.__io).startReviewer()
        self.__domainRex = re.compile(r'http(s)?://([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*')
        self.__cnDomainRex = re.compile(r'\.cn(/)?$')
        self.__topDomainRex = re.compile(r'\w+\.\w+$')
        self.__getLastTimeList()

        # self.__domainSeeds = self.__getSeeds()

    def __del__(self):
        f = codecs.open('./domainlist.txt','w','utf-8')
        for domian in self.__domainList:
            f.write(domian + '\n')
        f.close()

    def __getLastTimeList(self):
        try:
            f = codecs.open('./domainlist.txt', 'r','utf-8')
            for line in f.readlines():
                line = line.strip('\n')
                self.__domainList.append(line)
            f.close()

        except:
            pass

#以一个域名数组为种子开始爬
    def start(self):
        i = 0
        while i < 15:
            self.__nextPage()
            i = i+1
#准备种子,如果是第一次启动则使用字面量启动
    def __getSeeds(self):
        return ['www.hao123.com']
    #获取链接列表里的下一个页面
    def __nextPage(self):
        if len(self.__domainList) == 0:
            self.__domainList = self.__getSeeds()
            print(self.__domainList)

        url = self.__domainList.pop(0)
        if self.__pingDomain(url):
            pageContent = self.__getPage(url)
            topDomain = self.__topDomainRex.findall(url)

            self.__io.saveDomain(topDomain[0])
            self.__gatherDomainFromPage(pageContent)





    def __gatherDomainFromPage(self,page):
        if len(self.__domainList) > 5000:
            return
        try:
            m = self.__domainRex.findall(page)
        except:
            print('Get wrong data! skip it!')
            return

        domainList = []
        if m:
            for domain in m:
                domainList.append(domain[1])
        domainList = self.__deDuplicate(domainList)
        domainList = self.__checkDomainFromList(domainList)
        self.__domainList += domainList



    def __checkDomainFromList(self,list):
        domainList = []

        for domain in list:
            m = self.__cnDomainRex.findall(domain)
            if m:
                continue
            else:

                domainList.append(domain)

        return domainList

    def __getPage(self,url):
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',  # Force certificate check.
            ca_certs=certifi.where(),  # Path to the Certifi bundle.
        )
        data = ''
        try:
            data = http.request('GET', url, timeout=10).data
            codeType = chardet.detect(data)
            data = data.decode(codeType['encoding'])
        except:
            print('Get url:'+url+' error! ----Maby page encoding detect wrong')
        return data

    def __pingDomain(self,domain):
        cmd = "ping -c 1 " + domain
        args = shlex.split(cmd)

        try:
            subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False


    def __deDuplicate(self,list):
        result = []
        for item in list:
            try:
                result.index(item)
            except:
                result.append(item)
        return result


