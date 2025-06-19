
# file name : dashboard.py
# this file contains interactive dashboard that allows users to input an RTSP stream or choose from example video links, specify frame rate and image saving interval, and then start or stop the stream and image capturing process
# When the "Start" button is clicked, it initiates both video streaming and image saving
#  the "Stop" button stops image saving. The gallery component displays  recently saved images from the local folder , with a refresh button to update it manually

import gradio as gr
import glob
import os
from stream_utilis import video_stream_HIKvision
from image_saver import start_periodic_image_saving, stop_periodic_image_saving

#  example of  video paths
example_videos_folder = "./example_videos"
EXAMPLE_VIDEOS_LIST = os.listdir(example_videos_folder)
EXAMPLE_VIDEOS_LIST = [os.path.join(example_videos_folder, v) 
                       for v in EXAMPLE_VIDEOS_LIST + [
                        'rtsp://admin:Admin123@192.168.254.200:554/Streaming/Channels/101', 
                        'rtsp://admin:Admin123@192.168.254.201:554/Streaming/Channels/101', 
                        'rtsp://admin:Admin123@192.168.254.202:554/Streaming/Channels/101', 
                        'rtsp://admin:Admin123@192.168.254.203:554/Streaming/Channels/101'
                        ]]

# Function to show recent images from data/captured_images
def get_recent_images_gallery(n=10): # showing only 10 latest images based on the timestamps
    images = sorted(glob.glob("data/captured_images/*.jpg"), key=os.path.getmtime, reverse=True)
    return images[:n]

with gr.Blocks() as demo:
    gr.Markdown("# 📷 Hikvision Data Collection Pipeline")

    # Inputs
    rtsp_input = gr.Textbox(label="RTSP Address or Video File Path")
    frame_rate_input = gr.Textbox(label="Frame Rate (FPS)", value="5")
    save_interval = gr.Slider(minimum=1, maximum=60, value=5, label="Save Image Every (Seconds)")
    
    gr.Examples(
        examples=[[v] for v in EXAMPLE_VIDEOS_LIST],
        inputs=[rtsp_input],
        label="🎬 Example Videos (Click to Load)",
    )

    #  main buttons ( starting , stopping , refreshing the gallery )
    start_btn = gr.Button("▶ Start")
    stop_btn = gr.Button("⏹ Stop")
    refresh_btn = gr.Button("🔄 Refresh Image Gallery")

    # Outputs
    live_frame = gr.Image(label="Live Feed")
    status = gr.Textbox(label="Status")
    gallery = gr.Gallery(label="Captured Images", show_label=True)

    # Start both stream and saving
    start_btn.click(fn=video_stream_HIKvision,
                    inputs=[rtsp_input, frame_rate_input],
                    outputs=live_frame)

    start_btn.click(fn=start_periodic_image_saving,
                    inputs=[save_interval],
                    outputs=status)
    # Stop saving
    stop_btn.click(fn=stop_periodic_image_saving,
                   outputs=status)

    # Refresh captured images
    refresh_btn.click(fn=get_recent_images_gallery,
                      outputs=gallery)

demo.launch()

