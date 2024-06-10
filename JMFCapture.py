import cv2


class JMFCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    def is_opened(self):
        return self.cap.isOpened()

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()
