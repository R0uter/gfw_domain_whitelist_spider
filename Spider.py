import urllib3
import certifi
import re
import subprocess
import shlex
import codecs
import chardet
import threading
import dns.resolver
import isChinaIP



class Spider:
    __domainList = []
    __whiteList = []

    def __init__(self,ioMethod):
        self.__io = ioMethod

        self.__domainRex = re.compile(r'http(s)?://([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*')
        self.__cnDomainRex = re.compile(r'\.cn(/)?$')
        self.__topDomainRex = re.compile(r'\w+\.\w+$')
        self.__getLastTimeList()
        self.__lock = threading.Lock()
        self.__resolver = dns.resolver.Resolver()
        self.__resolver.nameservers = ['223.5.5.5','223.6.6.6']
        self.__chinaIP = isChinaIP.ChinaIP()
        
        # self.__domainSeeds = self.__getSeeds()

    def __cache(self):

        f = codecs.open('./domainlistCache','w','utf-8')

        for domian in self.__domainList:
            f.write(domian + '\n')
        f.close()

    def __getLastTimeList(self):
        try:
            f = codecs.open('./domainlistCache', 'r','utf-8')
            for line in f.readlines():
                line = line.strip('\n')
                self.__domainList.append(line)
            f.close()

        except:
            pass


    def start(self):


        self.__domainList = self.__getSeeds()
        # self.__cache()

        while True:
            threads = []

            self.__cache()
            for thread in range(20):
                threads.append(threading.Thread(target=self.__nextPage))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            # print('Process next N pages...')



    def __getSeeds(self):
        return ['www.hao123.com']

    def __nextPage(self):
        self.__lock.acquire()
        if len(self.__domainList) == 0:
            self.__domainList = self.__getSeeds()
            # print(self.__domainList)
        url = self.__domainList.pop(0)
        self.__lock.release()

        if self.__pingDomain(url):

            if self.__isWellKnown(url) : return
            #skip this domain if wellknowen
            pageContent = self.__getPage(url)
            topDomain = self.__topDomainRex.findall(url)
            self.__lock.acquire()
            self.__io.saveDomain(topDomain[0])
            self.__lock.release()
            self.__gatherDomainFromPage(pageContent)

    def __gatherDomainFromPage(self,page):
        if len(self.__domainList) > 10000:
            return
        try:
            m = self.__domainRex.findall(page)
        except:
            #print('Get wrong data! skip it!')
            return

        domainList = []
        if m:
            for domain in m:
                domainList.append(domain[1])
        domainList = self.__deDuplicate(domainList)
        domainList = self.__checkDomainFromList(domainList)
        self.__lock.acquire()
        self.__domainList += domainList
        self.__lock.release()


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
            data = http.request('GET', url, timeout=10,
                                headers={
                                    'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
                                ).data

            codeType = chardet.detect(data)
            data = data.decode(codeType['encoding'])
        except:
            pass

        return data

    def __pingDomain(self,domain):
        a = []
        isAvailable = True
        try:
            a = self.__resolver.query(domain)
        except:
            isAvailable = False
        if len(a) == 0:return False
        ip = str(a[0])
        if self.__chinaIP.isChinaIP(ip):

            cmd = "ping -c 1 " + ip
            args = shlex.split(cmd)

            try:
                subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            except subprocess.CalledProcessError:
                isAvailable = False
        else:
            isAvailable = False

        return isAvailable


    def __deDuplicate(self,list):
        result = []
        for item in list:
            try:
                result.index(item)
            except:
                result.append(item)
        return result

    def __isWellKnown(self,domain):
        topDomain = self.__topDomainRex.findall(domain)
        self.__lock.acquire()
        result = self.__io.getDomainRank(topDomain)
        self.__lock.release()
        return result > 2000

