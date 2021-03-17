import pymysql
from pymysql.connections import Connection
from datetime import datetime

#mySQL = sql(user='root', passwd='1234', host='127.0.0.1', db ='frames')

class MySQL:

    def __init__(self, user, passwd, host, db, charset='utf8'):
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__db = db
        self.__charset = charset
        self.__conn : Connection = None

    def __connect(self):
        if self.__conn is None:
            self.__conn = pymysql.connect(
                            user = self.__user, 
                            passwd = self.__passwd,
                            host = self.__host,
                            db = self.__db,
                            charset = self.__charset)

    def __disconnect(self):
        if self.__conn is not None:
            self.__conn.close()
    
    def insertStatus(self, state, facilityNum, memberNum, temperature, regData= datetime.now(), tableName = "status"):
        try:
            self.__connect()
            cursor = self.__conn.cursor()
        
            # regdate, state, facility_bno, member_mno, temperature
            query = f"""
            INSERT INTO {tableName} (regdate, state, facility_bno, member_mno, temperature) 
            VALUES ("{regData}",{state},{facilityNum},{memberNum},{temperature})
            """
            cursor.execute(query)
        
            self.__conn.commit()
        
        finally:
            self.__disconnect()

