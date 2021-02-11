import face_recognition
import glob
import numpy as np

class FaceTool():
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        path = "server/resources/imgs/"
        imgs = glob.glob(path+"*")
        for img in imgs:
            ext = img.split(".")[-1]
            label = img[len(path):-len(ext)-1]
            self.registerImage(label, img)
    
    def registerImage(self, label, imgPath):
        try:
            image = face_recognition.load_image_file(imgPath)
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(label)
            print("reg img: %s(%s)"%(label, imgPath))
            # print(face_encoding)
            pass
        except IndexError:
            print("failed to reg img: %s(%s)"%(label, imgPath))
            pass

    def match(self, face_encoding):
        name = "Unknown"
        # matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        print(face_distances)
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] <= 0.5:
            name = self.known_face_names[best_match_index]
        
        return name, int(best_match_index), float(face_distances[best_match_index])


