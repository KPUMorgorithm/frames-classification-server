import face_recognition
import glob
import numpy as np

class FaceTool():
    def __init__(self):
        self.known_face = []
        path = "server/resources/classes/"
        classes = glob.glob(path+"*")
        for label in classes:
            imgs = glob.glob(label+"/*")
            label = label.split("/")[-1]
            print(label)
            for img in imgs:
                self.registerImage(label, img)
    
    def registerImage(self, label, imgPath):
        try:
            image = face_recognition.load_image_file(imgPath)
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_face.append((label, face_encoding))
            print("reg img: %s(%s)"%(label, imgPath))
        except IndexError:
            print("failed to reg img: %s(%s)"%(label, imgPath))

    @staticmethod
    def feature(frame):
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=0)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        return (face_locations, face_encodings)

    def match(self, face_encoding):
        name = "Unknown"

        # matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
        face_distances = face_recognition.face_distance(list(map(lambda x: x[1], self.known_face)), face_encoding)
        print(face_distances)
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] <= 0.5:
            name = self.known_face[best_match_index][0]
        
        return name, float(face_distances[best_match_index])


