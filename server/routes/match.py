from face_recognition.api import face_encodings
import numpy as np
import cv2
from flask import request, Blueprint
from server.tools.face_tool import FaceTool
from server.tools.face_detector import FaceDetector
from server.tools.mask_detector import MaskDetector

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
            
            (name, face_distance) = ft.match(faceEncoding)
            result.append(( 0,
                            name,
                            (top,right,bottom,left)
                          ))
            
    return {'data': result}, 200