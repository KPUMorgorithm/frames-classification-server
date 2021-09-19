from datetime import datetime, timedelta
import traceback

class StatusRepository:
    def __init__(self, db):
        self.__db = db
    
    def initAutoIncrement(self):
        try:    
            with self.__db.getConnection() as conn:
                with conn.cursor() as cursor:
                    sql = "ALTER TABLE status AUTO_INCREMENT=1"
                    cursor.execute(sql)
                conn.commit()
                with conn.cursor() as cursor:
                    sql = "set @cnt = 0"
                    cursor.execute(sql)
                conn.commit()
                with conn.cursor() as cursor:
                    sql = 'update status set status.statusnum = @cnt:=@cnt+1'
                    cursor.execute(sql)
                conn.commit()
                
        except Exception as e:
            traceback.print_exc()

    def insertStatus(self, state, facilityNum, memberNum, temperature, regdate=datetime.now()):
        regdate = regdate + timedelta(hours=9)
        print(regdate)
        self.initAutoIncrement()
        try:    
            with self.__db.getConnection() as conn:
                with conn.cursor() as cursor:
                    sql = f'INSERT INTO status(state, facility_bno, member_mno, temperature, regdate) VALUES ({state}, {facilityNum}, {memberNum}, {temperature}, "{regdate}")'
                    cursor.execute(sql)
                conn.commit()

        except Exception as e:
            traceback.print_exc()