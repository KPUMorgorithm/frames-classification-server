import face_recognition
import glob
import numpy as np
from .face_list import FaceList


class FaceTool():
    def __init__(self):
        self.faceList = FaceList(3,"server/tools/faceData")

        self.contextFaceList = self.faceList.getListByQueue()
    
    # @staticmethod
    # def feature(frame):
    #     rgb_frame = frame[:, :, ::-1]

    #     face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=0)
    #     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
    #     return (face_locations, face_encodings)

    def match(self, landmark):
        name = "Unknown"
        face_distances = face_recognition.face_distance(list(map(lambda x: x[1], self.contextFaceList)), self.__convertListLandmark(landmark))
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] <= 0.5:
            name = self.contextFaceList[best_match_index][0]
        
        return name, float(face_distances[best_match_index])

    def __convertListLandmark(self, listLandmark):
        print(listLandmark)
        return np.array(listLandmark)
