from datetime import datetime, timedelta
import traceback

class MemberRepository:
    def __init__(self, db):
        self.__db = db

    def getMembers(self):
        try:    
            with self.__db.getConnection() as conn:
                with conn.cursor() as cursor:
                    sql = f'SELECT * FROM member'
                    cursor.execute(sql)
                    conn.commit()
                    return cursor.fetchall()

        except Exception as e:
            traceback.print_exc()
            return []
            
    def getMemberImages(self, mno):
        try:    
            with self.__db.getConnection() as conn:
                with conn.cursor() as cursor:
                    sql = f'SELECT * FROM member_image WHERE member_mno={mno}'
                    cursor.execute(sql)
                    conn.commit()
                    return cursor.fetchall()

        except Exception as e:
            traceback.print_exc()
            return []

    def getMembersWithImages(self):
        _members = self.getMembers()

        members = []
        for member in _members:
            _member_images = self.getMemberImages(mno=member[0])
            images = []
            for member_image in _member_images:
                images.append({
                    "id": member_image[0],
                    "name": member_image[1],
                    "path": member_image[2],
                    "uuid": member_image[3]
                })
            members.append({
                "mno": member[0],
                "name": member[1],
                "phone": member[2],
                "images": images
            })

        print(members)
        return members