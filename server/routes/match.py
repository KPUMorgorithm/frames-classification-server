import numpy as np
import cv2
from flask import request, Blueprint
from server.tools.face_tool import FaceTool
import face_recognition

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

ft = FaceTool()
bp = Blueprint('match', __name__, url_prefix='/match')

model = load_model('server/mask_detector.model')
net = cv2.dnn.readNet('server/face_detector/deploy.prototxt','server/face_detector/res10_300x300_ssd_iter_140000.caffemodel')

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

        
        # Face Mask Detection 정제과정
        (h, w) = np.shape(frame)[:2]
        (top, right, bottom, left) = face_location
        top = max(0,top)
        bottom = min(h-1,bottom)
        left = max(0,left)
        right = min(w-1,right)

        face = frame[top:bottom,left:right]
        face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)
        face = np.expand_dims(face, axis=0)

        
        (mask,withoutMask) = model.predict(face)[0]
        if mask>withoutMask:
            print("Mask")
        else:
            print("No Mask")

        print(name,"Mask:",mask,"No Mask: ",withoutMask)
        # Face Mask Detection 정제과정 끝
    '''

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0)) #프레임을 blob 화
    net.setInput(blob)
    detections = net.forward()

    (h, w) = np.shape(frame)[:2]

    for i in range(0, detections.shape[2]):
        confidence = detections[0,0,i,2]

        if confidence < 0.5: #임계점 이하일시 continue
            continue
        
        #mask detection
        face_location = detections[0,0,i,3:7] * np.array([w,h,w,h])
        (left, top, right, bottom) = face_location.astype("int")
        top = max(0,top)
        bottom = min(h-1,bottom)
        left = max(0,left)
        right = min(w-1,right)        

        print(top,bottom,left,right)

        face = frame[top:bottom,left:right]
        face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)
        face = np.expand_dims(face, axis=0)

        (mask,withoutMask) = model.predict(face)[0]
        if mask>withoutMask:
            print("Mask")
            # --- TODO : 클라이언트에 마스크를 벗어달라는 메세지 출력

        else:
            print("No Mask")
            # --- TODO :         

    return {'data': result}, 200
