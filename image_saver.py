# # # file name : image_saver.py
# # #This file manages periodic saving of images from the video stream. 
# # It defines two main functions: start_periodic_image_saving() and stop_periodic_image_saving(). 
# # When started, it launches a background thread that runs independently and continuously checks the frame_stack for the latest frame.
# #  Every few seconds , it captures the current frame, converts it from RGB to BGR format, and saves it as a .jpg image when an object is detected with a timestamped filename in the data/captured_images directory.
## after
# #  The saving loop continues the stop button is clicked.

# import os
# import cv2
# import time
# from datetime import datetime
# import threading
# from stream_utilis import frame_stack
# from ultralytics import YOLO

# # Load YOLO model
# model = YOLO("yolov8s-world.pt")
# CUSTOM_CLASSES = ["one bird", "one airplane", "one kite", "a flying object"]
# model.set_classes(CUSTOM_CLASSES)

# SAVE_FOLDER = "data/captured_images"
# os.makedirs(SAVE_FOLDER, exist_ok=True)

# collecting_images = False

# def object_is_present(frame):
#     """
#     Returns True if the object is detected in the frame, False otherwise.
#     """
#     results = model.predict(frame, conf=0.25, verbose=False)
#     return len(results[0].boxes) > 0

# def start_periodic_image_saving(interval_seconds=2):
#     global collecting_images
#     collecting_images = True

#     def save_loop():
#         saving = False  
#         last_save_time = 0

#         while collecting_images:
#             if len(frame_stack) == 0:
#                 time.sleep(0.1)
#                 continue

#             frame = frame_stack[-1]

#             if object_is_present(frame):
#                 if not saving:
#                     print("[info] Object appeared, starting to save images.")
#                     saving = True

#                 # Save images every `interval_seconds`
#                 if time.time() - last_save_time >= interval_seconds:
#                     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                     filename = f"{SAVE_FOLDER}/image_{timestamp}.jpg"
#                     frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#                     cv2.imwrite(filename, frame_bgr)
#                     print(f"[saved] {filename}")
#                     last_save_time = time.time()
#             else:
#                 if saving:
#                     print("[info] Object disappeared, stopping save.")
#                 saving = False

#             time.sleep(0.1) 

#     t = threading.Thread(target=save_loop, daemon=True)
#     t.start()
#     return "Event-based image saving started"

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

# Background save settings
BACKGROUND_INTERVAL_SECONDS = 60  # Every 1 minute of capturing and saving images when an object is detected , it caputes and saves ten pictures consecutively irrespecgive whether an object is detected or not
NEUTRAL_FRAMES_TO_SAVE = 10
last_background_save_time = time.time()
background_saving = False
background_frame_count = 0

def object_is_present(frame):
    """
    Returns True if the object is detected in the frame, False otherwise.
    """
    results = model.predict(frame, conf=0.25, verbose=False)
    return len(results[0].boxes) > 0

def save_image(frame, prefix="image"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(SAVE_FOLDER, f"{prefix}_{timestamp}.jpg")
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, frame_bgr)
    print(f"[saved] {filename}")

def start_periodic_image_saving(interval_seconds=2):
    global collecting_images
    global last_background_save_time, background_saving, background_frame_count

    collecting_images = True

    def save_loop():
        global last_background_save_time, background_saving, background_frame_count
        saving_object_frames = False
        last_object_save_time = 0

        while collecting_images:
            if len(frame_stack) == 0:
                time.sleep(0.1)
                continue

            frame = frame_stack[-1]

            # Object-Triggered Saving 
            if object_is_present(frame):
                if not saving_object_frames:
                    print("[info] Object appeared, starting to save object frames.")
                    saving_object_frames = True

                if time.time() - last_object_save_time >= interval_seconds:
                    save_image(frame, prefix="object")
                    last_object_save_time = time.time()
            else:
                if saving_object_frames:
                    print("[info] Object disappeared, stopping object save.")
                saving_object_frames = False

            # Time-Based Background Frame Saving 
            current_time = time.time()
            if current_time - last_background_save_time >= BACKGROUND_INTERVAL_SECONDS:
                background_saving = True
                background_frame_count = 0
                last_background_save_time = current_time

            if background_saving:
                save_image(frame, prefix="neutral")
                background_frame_count += 1
                if background_frame_count >= NEUTRAL_FRAMES_TO_SAVE:
                    background_saving = False
                    print("[info] Finished background frame capture.")

            time.sleep(0.1)

    t = threading.Thread(target=save_loop, daemon=True)
    t.start()
    return "Event-based and timed image saving started"

def stop_periodic_image_saving():
    global collecting_images
    collecting_images = False
    return "Image saving stopped"
