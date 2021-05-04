from datetime import datetime, timedelta
import traceback

class StatusRepository:
    def __init__(self, db):
        self.__db = db
    
    def insertStatus(self, state, facility_bno, member_mno, temperature, regdate=datetime.now()):
            try:    
                with self.__db.getConnection() as conn:
                    with conn.cursor() as cursor:
                        sql = "INSERT INTO status(state, facility_bno, member_mno, temperature, regdate) VALUES (%s, %s, %s, %s, %s)"
                    conn.commit()

            except Exception as e:
                traceback.print_exc()