import cv2

for i in range(0, 10):
    cam = cv2.VideoCapture(i)
    ok, _ = cam.read()
    cam.release()
    print(i, ok)
