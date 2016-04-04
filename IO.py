import pymysql
import datetime

class IO:

    __DomainRank = 0
    __Domain = 1
    __LastUpdate = 2


    def __init__(self):

        host = '10.211.55.14'
        user = 'python'
        passwd = 'toor'
        db = 'whitelist'


        self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=3306, charset='utf8')

    def __del__(self):

        self.conn.close()


    def saveDomain(self,domain):
        self.__updateDomain(domain)



    def __updateDomain(self,domain):
        cur = self.conn.cursor()
        cur.execute('select * from WhiteList where Domain=%s',domain)
        data = cur.fetchall()
        if data:
            rank = data[0][self.__DomainRank]
            cur.execute('update WhiteList set DomainRank=%s,LastUpdate=%s where domain=%s',(rank + 1,datetime.datetime.now().strftime("%Y%m%d"),domain))
            self.conn.commit()
        else:
            cur.execute('insert into WhiteList (Domain,DomainRank,LastUpdate) values (%s,%s,%s)',(domain,1,datetime.datetime.now().strftime("%Y%m%d")))
            self.conn.commit()
        cur.close()



    def saveData(self,data):
        pass
    def getList (self):
        cur = self.conn.cursor()
        cur.execute('select * from WhiteList order by DomainRank desc')
        data = cur.fetchall()
        cur.close()
        return data

    def getDomainWithNumber(self,number):
        pass



