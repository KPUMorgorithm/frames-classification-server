import cv2
import numpy as np

from .face_tool import *

ft = FaceTool()

def startCapture():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret: break

        frame = cv2.flip(frame, 1)

        # TODO : 마스크 검증
        faces = ft.feature(frame)

        for name, top, right, bottom, left in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow("cam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
