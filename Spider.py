import Reviewer
import IO


#爬虫类
class Spider:
    __domainSeeds = []
    __linkList = []

    def __init__(self):

        self.__reviewer = Reviewer.Reviewer().startReviewer()
        self.__io = IO.IO.getIO()
        self.__domainSeeds = self.__getSeeds()





#以一个域名数组为种子开始爬
    def start(self):
        pass
#准备种子,如果是第一次启动则使用字面量启动
    def __getSeeds(self):
        pass
    #获取链接列表里的下一个页面
    def __nextWebPage(self):
        pass
#从页面里获取链接
    def __gatherLinksFromPage(self):
        pass
#检查链接列表里的域名
    def __checkDomainFromLinks(self):
        pass






