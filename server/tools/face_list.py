import pickle
from collections import deque
import glob
import face_recognition
import requests
from server.db.db import DB
import os
import shutil
import copy

class FaceList :
    WEIGHT: float = 0.9
    def __init__(self, queueSize, pickleName):
        self.__queueSize = queueSize
        self.__pickleName = pickleName
        self.__faceData: dict = self.loadDict()
        self.syncServer()
    
    def downloadImage(self, image):
        path = image["path"].replace("\\", "/")
        uuid = image["uuid"]
        name = image["name"]
        filename = f'{uuid}_{name}'
        url = f'http://test.outstandingboy.com:8080/image/{path}/{filename}'
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open("server/resources/tmp/"+filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                return "server/resources/tmp/"+filename

    def addImage(self, mno, image):
        try:
            imgPath = self.downloadImage(image)
            img = face_recognition.load_image_file(imgPath)
            os.remove(imgPath)
            faceEncoding = face_recognition.face_encodings(img)[0]
            # self._addDatainQueue(name,faceEncoding)
            self._updateData(mno, faceEncoding)
            if (self.__faceData[mno].get("images") is None):
                self.__faceData[mno]["images"] = []
            self.__faceData[mno]["images"].append(image)
            print("reg img: %s"%(mno))

        except IndexError:
            print("failed to reg img: %s"%(mno))

    def _updateData(self, mno, faceEncoding):
        if self.__faceData[mno].get("faceEncoding") is None:
            self.__faceData[mno]["faceEncoding"] = faceEncoding
        else:
            self.__faceData[mno]["faceEncoding"] = self.__faceData[mno]["faceEncoding"] * FaceList.WEIGHT + faceEncoding * (1-FaceList.WEIGHT)
    
    def getFaceDataList(self):
        retList = []
        for mno, data in self.__faceData.items():
            retList.append((mno, data))
        return retList

    def saveDict(self):
        with open(self.__pickleName,'wb') as f:
            pickle.dump(self.__faceData, f)

    def loadDict(self):
        try:
            with open(self.__pickleName,'rb') as f:
                return pickle.load(f)

        except FileNotFoundError:
            with open(self.__pickleName,'wb') as f:
                return {}
            
        except EOFError:
            return {}


    def syncServer(self):
        db = DB.instance()
        members = db.member.getMembersWithImages()

        # 서버에 존재하지 않는 멤버 데이터 제거
        for mno in self.__faceData.keys():
            exists = False
            for member in members:
                if member["mno"] == mno:
                    exists = True
                    break
            if not exists:
                del self.__faceData[mno]

        # 메모리에 존재하지 않는 멤버 데이터 추가 
        for member in members:
            mno = member["mno"]
            if mno not in self.__faceData:
                self.__faceData[mno] = copy.deepcopy(member)
                del self.__faceData[mno]["images"]
                for image in member["images"]:
                    self.addImage(mno, image)
                continue
            else: # 멤버는 존재하나 이미지가 반영되지 않은 경우
                for image in member["images"]:
                    if image not in self.__faceData[mno]["images"]:
                        self.addImage(mno, image)

        self.saveDict()

            # for image in member["images"]:
            #     if image not in self.__faceData[mno]["images"]:
            #         self.addImage(mno, image)
        


# f = FaceList(3,"faceData")
# f.addDefaultData()
# print(f.getListByQueue())
# f.saveDict()
