from face_recognition.api import face_encodings
import numpy as np
import cv2
from flask import request, Blueprint
from server.tools.face_tool import FaceTool
from server.tools.face_detector import FaceDetector
from server.tools.mask_detector import MaskDetector

from server.db.db import  DB

from server.store.checklistStore import Checklist, MemberDict

ft = FaceTool()
fd = FaceDetector('server/tools/face_detector/deploy.prototxt',
    'server/tools/face_detector/res10_300x300_ssd_iter_140000.caffemodel')
md = MaskDetector('server/tools/mask_detector.model')

bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('/', methods=['POST'], strict_slashes=False)
def match():

    db = DB.instance()
    result = []
    nparr = np.fromstring(request.files['frame'].read(), np.uint8) # 리퀘스트로 버퍼 읽기
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # 버퍼 -> Mat
    tp = request.form["temperature"] 
    fNum = request.form["facilityNum"]
    state = request.form["state"]

    for detection in fd.GetDetectionsFromFrame(frame):
        
        if fd.GetConfidence(detection) < 0.5: #임계점 이하일시 continue
            continue
        
        (mask,withoutMask) = md.MaskDetection(fd.GetFaceLocationForMD(detection, frame))
        
        if mask>withoutMask:
            print("Mask")
            result.append((False, None))

        else:
            print("No Mask")
            (left,top,right,bottom) = fd.GetFaceLocation(detection,frame)
            faceLocation = []
            faceLocation.append((top,right,bottom,left))
            faceEncoding = face_encodings(frame,faceLocation)[0]
            
            (name, face_distance) = ft.match(faceEncoding)
            result.append(( True,
                            name,
                          ))
                          
            # sql.insertStatus(state=state, facilityNum=fNum, memberNum=1, temperature=tp)
            checklist: MemberDict = Checklist.instance()
            checklist.check(1, ifNotExists=lambda: db.status.insertStatus(state=0, facilityNum=3, memberNum=1, temperature=tp, regdate=datetime.now() + timedelta(seconds=10)))
       
            print(f"tp = {tp}, fNum = {fNum}, state = {state}, name = {name}")

            
    return {'data': result}, 200