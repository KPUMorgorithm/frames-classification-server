from flask import Flask, g
import time

from .routes import match

from server.tools.mysql.mysql import SingletonSQL

#TODO: SQL Disconnect 타이밍을 모르겠음
SingletonSQL.instance(user='root', passwd='1234', host='127.0.0.1', db ='frames')

app = Flask(__name__)
app.register_blueprint(match.bp)

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(' --- done : %f '%diff)
    return response
