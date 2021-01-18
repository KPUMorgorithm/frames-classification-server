import face_recognition
import time
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
            pass
        except IndexError:
            print("failed to reg img: %s(%s)"%(label, imgPath))
            pass

    def feature(self, frame):
        rgb_frame = frame[:, :, ::-1]
    
        start = time.time()
        face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=0)
        print("#1: %f" % (time.time()-start))
        start = time.time()
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        print("#2: %f" % (time.time()-start))

        faces = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name, index, face_distance = self.match(face_encoding)
            print(name, index, face_distance)
            faces.append((name, top, right, bottom, left))

        return faces

    def match(self, face_encoding):
        name = "Unknown"

        # matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        print(face_distances)
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] <= 0.5:
            name = self.known_face_names[best_match_index]
        
        return name, best_match_index, face_distances[best_match_index]


