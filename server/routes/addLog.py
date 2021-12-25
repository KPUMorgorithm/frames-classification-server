from flask import request, Blueprint
from server.db.db import DB
from server.store.checklistStore import Checklist, MemberDict
import time
bp = Blueprint('addLog', __name__, url_prefix='/addLog')

# @bp.route('/test', methods=['GET'])
# def addLogTest():
#     db : DB = DB.instance()
#     checklist: MemberDict = Checklist.instance()
#     for i in range(20):
#         checklist.check(1
#             , ifNotExists=lambda: db.status.insertStatus(state=1, facility_bno=1, member_mno=1, temperature=36)
#             , ifExists=lambda: print("exists!!!!")
#         )
#         time.sleep(1)
#     return 'hi'

# @bp.route('/',methods=['POST'], strict_slashes=False)
# def addLog():
#     db : DB = DB.instance()

#     tp = request.form["temperature"] 
#     name = request.form["name"]
#     mNum = request.form["memberNum"]
#     fNum = request.form["facilityNum"]
#     state = request.form["state"]


#     checklist: MemberDict = Checklist.instance()
#     checklist.check(mNum, ifNotExists=lambda: db.status.insertStatus(state=state, facility_bno=fNum, member_mno=mNum, temperature=tp))

#     strs = tp + name + mNum + fNum + state 

#     return {'log': strs}, 200