from flask import request, Blueprint
from server.tools.mysql.mysql import  SingletonSQL

bp = Blueprint('addLog', __name__, url_prefix='/addLog')

@bp.route('/',methods=['POST'], strict_slashes=False)
def addLog():
    sql = SingletonSQL.instance()

    tp = request.form["temperature"] 
    name = request.form["name"]
    mNum = request.form["memberNum"]
    fNum = request.form["facilityNum"]
    state = request.form["state"]

            
    # 로그 기록
    # TODO: 건물 번호, 멤버 번호(check리스트로) 매핑 테이블이 있어야 함
    # TODO: state 0,1 구분 있어야 함
    # TODO: 온도 데이터 받아야 함
    sql.insertStatus(state=state, facilityNum=fNum, memberNum=mNum, temperature=tp)
            
    strs = tp + name + mNum + fNum + state 

    return {'log': strs}, 200