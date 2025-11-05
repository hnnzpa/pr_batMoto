import cv2
import os
from datetime import datetime
from pathlib import Path

folder = Path("C:/Users/Mateo/Documents/batman/pr_batMoto/fotos")
def hacer_foto(device_index=1, folder=Path("fotos")):
    cam = cv2.VideoCapture(device_index)

    ok, frame = cam.read()
    cam.release()
    
    if not ok:
        return False

    os.makedirs(folder, exist_ok=True)
    name = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    path = os.path.join(folder, name)
    cv2.imwrite(path, frame)
    return path
