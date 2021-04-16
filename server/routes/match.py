from face_recognition.api import face_encodings
import numpy as np
import cv2
from flask import request, Blueprint
from server.tools.face_tool import FaceTool
from server.tools.face_detector import FaceDetector
from server.tools.mask_detector import MaskDetector
from server.tools.mysql.mysql import  SingletonSQL

ft = FaceTool()
fd = FaceDetector('server/tools/face_detector/deploy.prototxt',
    'server/tools/face_detector/res10_300x300_ssd_iter_140000.caffemodel')
md = MaskDetector('server/tools/mask_detector.model')

bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('/', methods=['POST'], strict_slashes=False)


def match():
    sql = SingletonSQL.instance()

    result = []
    nparr = np.frombuffer(request.data, np.uint8) # 리퀘스트로 버퍼 읽기
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # 버퍼 -> Mat

    for detection in fd.GetDetectionsFromFrame(frame):
    
        if fd.GetConfidence(detection) < 0.5: #임계점 이하일시 continue
            continue
        
        (mask,withoutMask) = md.MaskDetection(fd.GetFaceLocationForMD(detection, frame))
        
        if mask>withoutMask:
            print("Mask")
            result.append((1, None, None))

        else:
            print("No Mask")
            (left,top,right,bottom) = fd.GetFaceLocation(detection,frame)
            faceLocation = []
            faceLocation.append((top,right,bottom,left))
            faceEncoding = face_encodings(frame,faceLocation)[0]
            
            # 로그 기록
            # TODO: 건물 번호, 멤버 번호(check리스트로) 매핑 테이블이 있어야 함
            # TODO: state 0,1 구분 있어야 함
            # TODO: 온도 데이터 받아야 함
            sql.insertStatus(state=1, facilityNum=1, memberNum=1, temperature=34.5)
            

            (name, face_distance) = ft.match(faceEncoding)
            result.append(( 0,
                            name,
                            (top,right,bottom,left)
                          ))
            
            
            
    return {'data': result}, 200