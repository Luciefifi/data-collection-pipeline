# file name : image_saver.py
#This file manages periodic saving of images from the video stream. 
# It defines two main functions: start_periodic_image_saving() and stop_periodic_image_saving(). 
# When started, it launches a background thread that runs independently and continuously checks the frame_stack for the latest frame.
#  Every few seconds , it captures the current frame, converts it from RGB to BGR format, and saves it as a .jpg image with a timestamped filename in the data/captured_images directory.
#  The saving loop continues the stop button is clicked.

# import os
# import cv2
# import time
# from datetime import datetime
# import threading
# from stream_utilis import frame_stack

# SAVE_FOLDER = "data/captured_images"
# os.makedirs(SAVE_FOLDER, exist_ok=True)

# collecting_images = False

# def start_periodic_image_saving(interval_seconds=5):
#     global collecting_images
#     collecting_images = True

#     def save_loop():
#         while collecting_images:
#             if len(frame_stack) > 0:
#                 frame = frame_stack[-1]
#                 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                 filename = f"{SAVE_FOLDER}/image_{timestamp}.jpg"
#                 frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#                 cv2.imwrite(filename, frame_bgr)
#                 print(f"[saved] {filename}")
#             time.sleep(interval_seconds)

#     t = threading.Thread(target=save_loop, daemon=True)
#     t.start()
#     return "Image saving started"

# def stop_periodic_image_saving():
#     global collecting_images
#     collecting_images = False
#     return "Image saving stopped"
import os
import cv2
import time
from datetime import datetime
import threading
from stream_utilis import frame_stack
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8s-world.pt")
CUSTOM_CLASSES = ["one bird", "one airplane", "one kite", "a flying object"]
model.set_classes(CUSTOM_CLASSES)

SAVE_FOLDER = "data/captured_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

collecting_images = False

def object_is_present(frame):
    """
    Returns True if the object is detected in the frame, False otherwise.
    """
    results = model.predict(frame, conf=0.25, verbose=False)
    return len(results[0].boxes) > 0

def start_periodic_image_saving(interval_seconds=2):
    global collecting_images
    collecting_images = True

    def save_loop():
        saving = False  
        last_save_time = 0

        while collecting_images:
            if len(frame_stack) == 0:
                time.sleep(0.1)
                continue

            frame = frame_stack[-1]

            if object_is_present(frame):
                if not saving:
                    print("[info] Object appeared, starting to save images.")
                    saving = True

                # Save images every `interval_seconds`
                if time.time() - last_save_time >= interval_seconds:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{SAVE_FOLDER}/image_{timestamp}.jpg"
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(filename, frame_bgr)
                    print(f"[saved] {filename}")
                    last_save_time = time.time()
            else:
                if saving:
                    print("[info] Object disappeared, stopping save.")
                saving = False

            time.sleep(0.1) 

    t = threading.Thread(target=save_loop, daemon=True)
    t.start()
    return "Event-based image saving started"

def stop_periodic_image_saving():
    global collecting_images
    collecting_images = False
    return "Image saving stopped"


