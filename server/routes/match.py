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
    
    '''    
    (face_locations, face_encodings) = ft.feature(frame) # FaceTool로 얼굴 위치랑 랜드마크 추출 

    for face_location, face_encoding in zip(face_locations, face_encodings):
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

    return {'data': result}, 200
