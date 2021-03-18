import time
from threading import Thread


#### db에서 member의 리스트를 딕셔너리형태로 받아와서 해당 클래스에 저장해야됨 

class CheckList:

    def __init__(self, cooldown = 60):
        self.__checkList = set()
        self.__cooldown = cooldown


    def isNotList(self, memberNum):

        if self.__checkList & {memberNum} == set() :
            return True
        return False

    def deleteList(self, memberNum):
        time.sleep(self.__cooldown)
        self.__checkList.remove(memberNum)
        
    def addList(self, memberNum):
        self.__checkList.add(memberNum)
        th = Thread(target=self.deleteList, args=(memberNum,))
        th.start()