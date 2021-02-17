import numpy as np
import cv2
from flask import request, Blueprint
from server.tools.face_tool import FaceTool

ft = FaceTool()
bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('/', methods=['POST'], strict_slashes=False)
def match():
    result = []
    nparr = np.frombuffer(request.data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    (face_locations, face_encodings) = ft.feature(frame)

    for face_location, face_encoding in zip(face_locations, face_encodings):
        (name, face_distance) = ft.match(face_encoding)
        print(name, face_distance)
        result.append((name, face_location))

    return {'data': result}, 200
