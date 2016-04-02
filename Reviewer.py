
#域名名单检查器
class Reviewer:
    __domainCount = 0
    __domainNumber = 0

    def __init__(self,ioMethod):
        self.__domainNumer = self.__getDomainNumber()
        self.__io = ioMethod

    def __del__(self):
        #记得保存当前检查位置
        self.__saveDomainNumber()
#从配置文件获取上次检查位置
    def __getDomainNumber(self):
        pass
    #启动检查器
    def startReviewer(self):
        pass
#检查下一个域名
    def __nextDomain(self):
        pass
#保存域名序号
    def __saveDomainNumber(self):
        pass