import cv2

#net = cv2.dnn.readNet('server/face_detector/deploy.prototxt','server/face_detector/res10_300x300_ssd_iter_140000.caffemodel')

class FaceDetector():
    def __init__(self, prototxt, model):
        self._net = cv2.dnn.readNet(prototxt, model)

    def GetDetectionsFromFrame(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300,300), (104.0,177.0,123.0))
        self.net.setInput(blob)
        return self.net.forward() #순방향 추론

    def NumberOfDection(detections):
        return range(0,detections.shape[2])
    
    def GetConfidence(detections, i):
        return detections[0,0,i,2]