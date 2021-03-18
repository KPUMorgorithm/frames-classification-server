import pymysql
from pymysql.connections import Connection
from datetime import datetime
from threading import Thread
import time
from server.tools.mysql.singletone import Singleton
from server.tools.mysql.checklist import CheckList
#mySQL = sql(user='root', passwd='1234', host='127.0.0.1', db ='frames')

class MySQL:

    def __init__(self, user, passwd, host, db, charset='utf8', cooldown=60):
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__db = db
        self.__charset = charset
        self.__cooldown = cooldown
        self.__conn : Connection = None
        self.__checkList = set()

    def __connect(self):
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
    
    #TODO: issubset 이 전부 True로 들어가짐
    def __isNotList(self, memberNum):

        if self.__checkList.issubset({memberNum}):
            print("issubset")
            return False
        print("notsubset")
        return True

    #TODO: __deleteList() argument after * must be an iterable, not int
    def __deleteList(self, memberNum):
        print("타이머 시작")
        time.sleep(self.__cooldown)
        self.__checkList.discard(memberNum)
        print("삭제 완료")

    def __addList(self, memberNum):
        self.__checkList.add(memberNum)
        th = Thread(target=self.__deleteList, args=(memberNum))
        th.start()

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
