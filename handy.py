import cv2
from HandPanel import HandPanel
from HandDetector import HandDetector

def nothing(x):
    pass

class Handy:
    def __init__(self):
        self.hand_panel = HandPanel()

    def run(self):
        self.hand_panel.run()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = HandDetector("gloveHSV.txt", 640, 480)

    # Crear la ventana de ajustes de HSV
    cv2.namedWindow('HSV Adjustments')
    cv2.createTrackbar('HMin', 'HSV Adjustments', 0, 179, nothing)
    cv2.createTrackbar('HMax', 'HSV Adjustments', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'HSV Adjustments', 0, 255, nothing)
    cv2.createTrackbar('SMax', 'HSV Adjustments', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'HSV Adjustments', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'HSV Adjustments', 0, 255, nothing)

    # Valores iniciales de HSV (según la imagen)
    cv2.setTrackbarPos('HMin', 'HSV Adjustments', 0)
    cv2.setTrackbarPos('HMax', 'HSV Adjustments', 179)
    cv2.setTrackbarPos('SMin', 'HSV Adjustments', 41)
    cv2.setTrackbarPos('SMax', 'HSV Adjustments', 255)
    cv2.setTrackbarPos('VMin', 'HSV Adjustments', 44)
    cv2.setTrackbarPos('VMax', 'HSV Adjustments', 204)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # valores actuales de las trackbars
        h_min = cv2.getTrackbarPos('HMin', 'HSV Adjustments')
        h_max = cv2.getTrackbarPos('HMax', 'HSV Adjustments')
        s_min = cv2.getTrackbarPos('SMin', 'HSV Adjustments')
        s_max = cv2.getTrackbarPos('SMax', 'HSV Adjustments')
        v_min = cv2.getTrackbarPos('VMin', 'HSV Adjustments')
        v_max = cv2.getTrackbarPos('VMax', 'HSV Adjustments')

        # los valores de HSV en tiempo real
        detector.hue_lower, detector.hue_upper = h_min, h_max
        detector.sat_lower, detector.sat_upper = s_min, s_max
        detector.val_lower, detector.val_upper = v_min, v_max

        detector.update(frame)
        detector.draw(frame)

        cv2.imshow("Hand Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
