import os
import cv2
import time
from datetime import datetime
import threading
from stream_utilis import frame_stack

SAVE_FOLDER = "data/captured_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

collecting_images = False

def start_periodic_image_saving(interval_seconds=5):
    global collecting_images
    collecting_images = True

    def save_loop():
        while collecting_images:
            if len(frame_stack) > 0:
                frame = frame_stack[-1]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{SAVE_FOLDER}/image_{timestamp}.jpg"
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite(filename, frame_bgr)
                print(f"[saved] {filename}")
            time.sleep(interval_seconds)

    t = threading.Thread(target=save_loop, daemon=True)
    t.start()
    return "Image saving started"

def stop_periodic_image_saving():
    global collecting_images
    collecting_images = False
    return "Image saving stopped"
