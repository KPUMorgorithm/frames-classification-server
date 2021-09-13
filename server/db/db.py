import pymysql
from pymysql.connections import Connection

from server.type.singletone import Singleton
from server.db.repository.status import StatusRepository
from server.db.repository.member import MemberRepository

#mySQL = sql(user='root', passwd='1234', host='127.0.0.1', db ='frames')
class MySQL:
    def __init__(self, user, passwd, host, db, charset='utf8'):
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__db = db
        self.__charset = charset
        self.__conn : Connection = None
        self.status = StatusRepository(self)
        self.member = MemberRepository(self)

        self.connect()
    
    def getConnection(self):
        return pymysql.connect(
                        user = self.__user, 
                        port = 30000,
                        passwd = self.__passwd,
                        host = self.__host,
                        db = self.__db,
                        charset = self.__charset)

    def connect(self):
        if self.__conn is None:
            self.__conn = pymysql.connect(
                            user = self.__user, 
                            port = 30000,                
                            passwd = self.__passwd,
                            host = self.__host,
                            db = self.__db,
                            charset = self.__charset)
            
            print("connect()")

    def disconnect(self):
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None
            print("disconnected()")
    
class DB(MySQL, Singleton):
    pass
