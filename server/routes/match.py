from face_recognition.api import face_encodings, face_locations
import numpy as np
import cv2
from flask import request, Blueprint
from server.tools.face_tool import FaceTool
from server.tools.face_detector import FaceDetector
from server.tools.mask_detector import MaskDetector
import face_recognition

ft = FaceTool()
fd = FaceDetector('server/tools/face_detector/deploy.prototxt',
    'server/tools/face_detector/res10_300x300_ssd_iter_140000.caffemodel')
md = MaskDetector('server/tools/mask_detector.model')

bp = Blueprint('match', __name__, url_prefix='/match')


@bp.route('/', methods=['POST'], strict_slashes=False)
def match():
    result = []
    nparr = np.frombuffer(request.data, np.uint8) # 리퀘스트로 버퍼 읽기
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # 버퍼 -> Mat
    #frame = frame[:, :, ::-1]
    '''  
    (face_locations, face_encodings) = ft.feature(frame) # FaceTool로 얼굴 위치랑 랜드마크 추출 

    for face_location, face_encoding in zip(face_locations, face_encodings):
        (top,right,bottom,left) = face_location
        print(top,right,bottom,left)
        (name, face_distance) = ft.match(face_encoding)
        print(name, face_distance)
        result.append((name, face_location))
    '''
    

    
    for detection in fd.GetDetectionsFromFrame(frame):
    
        if fd.GetConfidence(detection) < 0.5: #임계점 이하일시 continue
            continue
        
        (mask,withoutMask) = md.MaskDetection(fd.GetFaceLocationForMD(detection, frame))
        
        if mask>withoutMask:
            print("Mask")
            # --- TODO : 클라이언트에 마스크를 벗어달라는 메세지 출력

        else:
            print("No Mask")
            # --- TODO : 클라이언트에서 열 측정과 face recognition 결과 출력
            # Issue: face recognition으로 로케이션 뽑을때랑 사람찾는거로 뽑은 로케이션이랑 살짝 다름
            # 그거때문인지 unknown으로 계속 찾게됨
            # 여기서 아예 face location에 있는 모델을 쓰면 부하가 조금 늘어날듯
            
            (left,top,right,bottom) = fd.GetFaceLocation(detection,frame)
            faceLocation = []
            faceLocation.append((top,right,bottom,left))
            faceEncoding = face_recognition.face_encodings(frame,faceLocation)[0]
            
            (name, face_distance) = ft.match(faceEncoding)
            print(name, face_distance)                      
            result.append((name,(top.item(),right.item(),bottom.item(),left.item())))
            
    return {'data': result}, 200