from flask import Flask, g
import time

# import os
# os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.0/bin")

from server.db.db import DB
DB.instance(user='admin', passwd='kpu123456!', host='framesdb.cys6irkoowji.ap-northeast-2.rds.amazonaws.com', db ='frames')
# DB.instance(user='admin', passwd='kpu123456!', host='localhost', db ='frames')

from server.tools.face_tool import FaceTool
FaceTool.instance(init=True)

from server.routes import match
from server.routes import addLog
from server.routes import sync

from server.scheduler.mainScheduler import MainScheduler, Scheduler, Task
from server.store.checklistStore import Checklist, MemberDict

checklist : MemberDict = Checklist.instance()

mainScheduler : Scheduler = MainScheduler.instance()
mainScheduler.addTask(Task(id='checklist', runnable=checklist.tick))

app = Flask(__name__)
app.register_blueprint(match.bp)
app.register_blueprint(addLog.bp)
app.register_blueprint(sync.bp)

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(' --- done : %f '%diff)
    return response