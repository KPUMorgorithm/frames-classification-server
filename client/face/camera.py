import cv2
import time
import numpy as np
import face_recognition
import requests


def startTest():
    while True:
        frame = cv2.imread('server/resources/imgs/ralo.jpg')
        # TODO : 마스크 검증
        faces = feature(frame)

        for name, top, right, bottom, left in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow("cam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def feature(frame):
    rgb_frame = frame[:, :, ::-1]

    # start = time.time()
    face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=0)
    # print("#1: %f" % (time.time()-start))
    # start = time.time()
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    # print("#2: %f" % (time.time()-start))

    # return face_locations, face_encodings
    faces = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        data = { 'features': face_encoding }
        t = time.time()
        res = requests.post('http://127.0.0.1:5000/match', data=data)
        print('request time :', time.time() - t)
        data = res.json()['data']

        (name, index, face_distance) = data # TODO : 서버에 요청

        print(name, index, face_distance)
        faces.append((name, top, right, bottom, left))

    return faces

def startCapture():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret: break

        frame = cv2.flip(frame, 1)

        # TODO : 마스크 검증
        faces = feature(frame)

        for name, top, right, bottom, left in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow("cam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
