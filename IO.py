
class IO:


    def __init__(self):
        self.__self = self
    #一个单件模式,确保全局只有一个IO对象
    #有错误，得改改。
    def getIO(self):
       if (self.__self == None) :
           self.__init__()
       else:
           return self.__self

    def saveDomain(self,domain):
        pass
    def saveData(self,data):
        pass
    def getData(self):
        pass
    def getDomainWithNumber(self,number):
        pass



