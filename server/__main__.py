import numpy as np
import time
from flask import Flask, request, g
from server.face_tool import FaceTool
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
ft = FaceTool()

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(' --- done : %f '%diff)
    return response

@app.route('/match', methods=['POST'])
def match():
    data = request.form.to_dict(flat=False)
    features = np.array(data['features'], dtype=np.float64)
    result = ft.match(features)
    print(result)
    return {'data': result}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
    