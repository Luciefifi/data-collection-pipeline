import cv2
import numpy as np
import time
from collections import deque

# Define the width and height standards for the video stream
WIDTH_STANDARD = 640
HEIGHT_STANDARD = 480

frame_stack = deque(maxlen=2)
fall_back_frame = np.zeros((256, 256, 3), dtype=np.uint8)+127

def video_stream_HIKvision(video_address, frame_rate=""):
    if frame_rate.strip() == "":
        frame_rate = 2.0
    else:
        frame_rate = float(frame_rate)
    cap = cv2.VideoCapture(video_address, cv2.CAP_FFMPEG)

    while True:
        ret, frame = cap.read()
        if ret :
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_stack.append(
                cv2.resize(
                    frame,
                    (WIDTH_STANDARD, HEIGHT_STANDARD)

                )
            
            )
            yield frame
            time.sleep(1 / frame_rate)

        else:
            yield fall_back_frame