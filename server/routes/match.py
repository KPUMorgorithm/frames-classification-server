from datetime import datetime, timedelta
from flask import request, Blueprint
from server.tools.face_tool import FaceTool

from server.db.db import  DB

from server.store.checklistStore import Checklist, MemberDict

from server.tools.mask_detector import MaskDetector

import numpy as np
import cv2

ft = FaceTool()
md = MaskDetector('server/tools/mask_detector.model')
bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('/', methods=['POST'], strict_slashes=False)
def match():

    db = DB.instance()
    result = []

    nparr = np.fromstring(request.files['face'].read(), np.uint8)
    face = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    tp = request.form["temperature"]
    fNum = request.form["facilityNum"]
    state = request.form["state"]

    if md.isMasked(face):
        result.append(True)
        result.append("")

    else:
        landmark = ft.feature(face)

        name, distance = ft.match(landmark)
        print(f"distance: {distance}")
        
        result.append(False)
        result.append(name)

        checklist: MemberDict = Checklist.instance()
        checklist.check(1, ifNotExists=lambda: db.status.insertStatus(state=0, facilityNum=3, memberNum=1, temperature=tp, regdate=datetime.now() + timedelta(seconds=10)),ifExists=None)

        print(f"tp = {tp}, fNum = {fNum}, state = {state}, name = {name}")

    return {'data': result}, 200