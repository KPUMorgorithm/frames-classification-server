import time
from apscheduler.schedulers.background import BackgroundScheduler
from server.scheduler.task import Task
from typing import List
from server.type.singletone import Singleton

class Scheduler:
    def __init__(self):
        self.__sched = BackgroundScheduler()
        self.__sched.add_job(self.__tick, 'interval', seconds=1, id='mainTask')
        self.__sched.start()
        self.__tasks : List[Task] = []

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.__sched.shutdown()

    def __tick(self):
        for task in self.__tasks:
            task.run()
    
    def addTask(self, task):
        self.__tasks.append(task)

    def delTask(self, tid):
        self.__tasks = filter(lambda task: task.id != tid, self.__tasks)

class MainScheduler(Scheduler, Singleton):
    pass