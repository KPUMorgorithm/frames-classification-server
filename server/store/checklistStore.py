from server.type.singletone import Singleton
from collections.abc import Callable

class MemberDict(dict):
    def __init__(self):
        super().__init__()

    def exists(self, memberNum):
        return memberNum in self.keys()

    def set(self, memberNum, seconds=10):
        self[memberNum] = seconds
        print("MemberDict: add member", memberNum, seconds)

    def tick(self):
        for memberNum in set(self.keys()):
            self[memberNum] -= 1
            if self[memberNum] < 0: 
                self.pop(memberNum)
                print("MemberDict: pop member", memberNum)
    
    def check(self, memberNum, ifNotExists: Callable, ifExists: Callable, seconds=10):
        if self.exists(memberNum):
            if ifExists != None: ifExists()
        else: 
            if ifNotExists != None: 
                ifNotExists()
                self.set(memberNum, seconds)

class Checklist(MemberDict, Singleton):
    pass