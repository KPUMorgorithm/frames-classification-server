import pymysql
from pymysql.connections import Connection
from datetime import datetime

from server.tools.mysql.singletone import Singleton
from server.tools.mysql.checklist import CheckList

#mySQL = sql(user='root', passwd='1234', host='127.0.0.1', db ='frames')

class MySQL:
    
    def __init__(self, user, passwd, host, db, charset='utf8'):
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__db = db
        self.__charset = charset
        self.__conn : Connection = None
        self.__checkList = CheckList()

        self.connect()

    def connect(self):
        if self.__conn is None:
            self.__conn = pymysql.connect(
                            user = self.__user, 
                            passwd = self.__passwd,
                            host = self.__host,
                            db = self.__db,
                            charset = self.__charset)
            
            print("connect()")

    def disconnect(self):
        if self.__conn is not None:
            self.__conn.close()
            print("disconnected()")
    

    def __insertStatus(self, state, facilityNum, memberNum, temperature, regData, tableName):
        try:    
            cursor = self.__conn.cursor()
        
            # column: regdate, state, facility_bno, member_mno, temperature
            query = f"""
            INSERT INTO {tableName} (regdate, state, facility_bno, member_mno, temperature) 
            VALUES ("{regData}",{state},{facilityNum},{memberNum},{temperature})
            """
            cursor.execute(query)
            self.__conn.commit()
        except:
            print("ERROR: INSERT QUERY")


    def insertStatus(self, state, facilityNum, memberNum, temperature, tableName = "status"):
        
        if self.__checkList.isNotList(memberNum):
            
            self.__insertStatus(state,facilityNum, memberNum, temperature, datetime.now(), tableName)
            print("insertStatus()")
            self.__checkList.addList(memberNum)
            print("addList")



class SingletonSQL(MySQL, Singleton):
    pass
