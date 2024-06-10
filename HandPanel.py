import cv2
from HandDetector import HandDetector
from JMFCapture import JMFCapture

class HandPanel:
    def __init__(self):
        self.detector = HandDetector("gloveHSV.txt", 640, 480)
        self.capture = JMFCapture()

    def run(self):
        while self.capture.is_opened():
            frame = self.capture.get_frame()
            if frame is None:
                break
            self.detector.update(frame)
            self.detector.draw(frame)
            cv2.imshow("Hand Detector", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.capture.release()
        cv2.destroyAllWindows()
