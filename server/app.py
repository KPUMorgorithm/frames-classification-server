from flask import Flask, g
import time

from .routes import match

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