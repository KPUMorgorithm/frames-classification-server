import pickle
from collections import deque
import glob
import face_recognition

class FaceList :
    def __init__(self, queueSize, pickleName):
        self.__queueSize = queueSize
        self.__pickleName = pickleName
        self.__queueDict = self.loadDict()

    def addImage(self, name, imgPath):
        try:
            image = face_recognition.load_image_file(imgPath)
            faceEncoding = face_recognition.face_encodings(image)[0]
            self._addDatainQueue(name,faceEncoding)

        except IndexError:
            print("failed to reg img: %s(%s)"%(name, imgPath))

    def _addDatainQueue(self, name, faceEncoding):
        q : deque = self._getQueueinDict(name)
        q.append(faceEncoding)

    def getListByQueue(self):
        retList = []
        for name, q in self.__queueDict.items():
            retList += self._getValuesInQueue(name, q)
        return retList
    
    def saveDict(self):
        with open(self.__pickleName,'wb') as f:
            pickle.dump(self.__queueDict, f)

    def loadDict(self):
        try:
            with open(self.__pickleName,'rb') as f:
                return pickle.load(f)

        except FileNotFoundError:
            return {}
            
        except EOFError:
            return {}

    def _getQueueinDict(self, name):
        if self.__queueDict.get(name) is None :
            self.__queueDict[name] = self._createNewQueue()
        
        return self.__queueDict.get(name)

    def _createNewQueue(self):
        return deque(maxlen = self.__queueSize)

    def _getValuesInQueue(self,name, q : deque):
        ret = []
        for elem in q:            
            ret.append((name,elem))           
        return ret
    
    def addDefaultData(self):
        classes = glob.glob("../resources/classes/*")

        for directoryPath in classes:
            imgPaths = glob.glob(directoryPath+"/*")
            name = directoryPath.split("\\")[-1]
            for path in imgPaths:
                self.addImage(name,path)
            print(f"{imgPaths} 완료")

# f = FaceList(3,"faceData")
# f.addDefaultData()
# print(f.getListByQueue())
# f.saveDict()
