from datetime import datetime, timedelta
from flask import request, Blueprint
from server.tools.face_tool import FaceTool

from server.db.db import  DB

from server.store.checklistStore import Checklist, MemberDict

ft = FaceTool()

bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('/', methods=['POST'], strict_slashes=False)
def match():

    db = DB.instance()
    result = []

    data = request.get_json()
    
    landmark = data["landmark"]
    tp = data["temperature"]
    fNum = data["facilityNum"]
    state = data["state"]

    name, _ = ft.match(landmark)
    result.append(name)
    # sql.insertStatus(state=state, facilityNum=fNum, memberNum=1, temperature=tp)
    checklist: MemberDict = Checklist.instance()
    checklist.check(1, ifNotExists=lambda: db.status.insertStatus(state=0, facilityNum=3, memberNum=1, temperature=tp, regdate=datetime.now() + timedelta(seconds=10)),ifExists=None)

    print(f"tp = {tp}, fNum = {fNum}, state = {state}, name = {name}")

            
    return {'data': result}, 200