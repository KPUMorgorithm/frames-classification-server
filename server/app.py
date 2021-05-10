from flask import Flask, g
import time

from server.routes import match
from server.routes import addLog

from server.db.db import DB
from server.scheduler.mainScheduler import MainScheduler, Scheduler, Task
from server.store.checklistStore import Checklist, MemberDict

DB.instance(user='admin', passwd='kpu123456!', host='framesdb.cys6irkoowji.ap-northeast-2.rds.amazonaws.com', db ='frames')

checklist : MemberDict = Checklist.instance()

mainScheduler : Scheduler = MainScheduler.instance()
mainScheduler.addTask(Task(id='checklist', runnable=checklist.tick))

app = Flask(__name__)
app.register_blueprint(match.bp)
app.register_blueprint(addLog.bp)

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(' --- done : %f '%diff)
    return response