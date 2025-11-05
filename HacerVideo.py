import cv2
import time
from pathlib import Path
from datetime import datetime

folder = Path("C:/Users/Mateo/Documents/batman/pr_batMoto/videos")
def hacer_video(device_index=1, folder = Path("videos")):
    folder.mkdir(parents=True, exist_ok=True)

    cam = cv2.VideoCapture(device_index)

    # leemos 1 frame para saber tamaño / fps
    ok, frame = cam.read()
    if not ok:
        cam.release()
        return None

    h, w = frame.shape[:2]

    # nombre archivo
    name = datetime.now().strftime("%Y%m%d_%H%M%S.avi")
    path = folder / name

    #  codec: MJPG que suele funcionar en Windows
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter(str(path), fourcc, 30, (w, h))

    t0 = time.time()
    while time.time() - t0 < 3:     # 3 segundos
        ok, frame = cam.read()
        if not ok:
            break
        out.write(frame)

    cam.release()
    out.release()
    return path
