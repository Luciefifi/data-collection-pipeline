# import gradio as gr
# import glob
# import os
# from stream_utilis import video_stream_HIKvision
# from image_saver import start_periodic_image_saving, stop_periodic_image_saving

# # Load example video paths
# example_videos_folder = "./example_videos"
# EXAMPLE_VIDEOS_LIST = os.listdir(example_videos_folder)
# EXAMPLE_VIDEOS_LIST = [os.path.join(example_videos_folder, v) 
#                        for v in EXAMPLE_VIDEOS_LIST]

# # Function to show recent images from data/captured_images
# def get_recent_images_gallery(n=10):
#     images = sorted(glob.glob("data/captured_images/*.jpg"), key=os.path.getmtime, reverse=True)
#     return images[:n]

# with gr.Blocks() as demo:
#     gr.Markdown("# 📷 Hikvision Data Collection Pipeline")

#     # Inputs
#     rtsp_input = gr.Textbox(label="RTSP Address or Video File Path")
#     frame_rate_input = gr.Textbox(label="Frame Rate (FPS)", value="5")
#     save_interval = gr.Slider(minimum=1, maximum=60, value=5, label="Save Image Every (Seconds)")
#     # Example video selector
#     gr.Examples(
#         examples=[[v] for v in EXAMPLE_VIDEOS_LIST],
#         inputs=[rtsp_input],
#         label="🎬 Example Videos (Click to Load)",
#     )
#     # Buttons
#     start_stream_btn = gr.Button("▶ Start Streaming")
#     start_save_btn = gr.Button("💾 Start Saving Images")
#     stop_save_btn = gr.Button("⏹ Stop Saving Images")
#     refresh_btn = gr.Button("🔄 Refresh Image Gallery")

#     # Outputs
#     live_frame = gr.Image(label="Live Feed")
#     status = gr.Textbox(label="Status")
#     gallery = gr.Gallery(label="Captured Images", show_label=True)



#     # Button logic
#     start_stream_btn.click(fn=video_stream_HIKvision,
#                            inputs=[rtsp_input, frame_rate_input],
#                            outputs=live_frame)

#     start_save_btn.click(fn=start_periodic_image_saving,
#                          inputs=[save_interval],
#                          outputs=status)

#     stop_save_btn.click(fn=stop_periodic_image_saving,
#                         outputs=status)

#     refresh_btn.click(fn=get_recent_images_gallery,
#                       outputs=gallery)

# demo.launch()

import gradio as gr
import glob
import os
from stream_utilis import video_stream_HIKvision
from image_saver import start_periodic_image_saving, stop_periodic_image_saving

# Load example video paths
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
def get_recent_images_gallery(n=10):
    images = sorted(glob.glob("data/captured_images/*.jpg"), key=os.path.getmtime, reverse=True)
    return images[:n]

with gr.Blocks() as demo:
    gr.Markdown("# 📷 Hikvision Data Collection Pipeline")

    # Inputs
    rtsp_input = gr.Textbox(label="RTSP Address or Video File Path")
    frame_rate_input = gr.Textbox(label="Frame Rate (FPS)", value="5")
    save_interval = gr.Slider(minimum=1, maximum=60, value=5, label="Save Image Every (Seconds)")
    
    # Example video selector
    gr.Examples(
        examples=[[v] for v in EXAMPLE_VIDEOS_LIST],
        inputs=[rtsp_input],
        label="🎬 Example Videos (Click to Load)",
    )

    # Two main buttons
    start_btn = gr.Button("▶ Start")
    stop_btn = gr.Button("⏹ Stop")
    refresh_btn = gr.Button("🔄 Refresh Image Gallery")

    # Outputs
    live_frame = gr.Image(label="Live Feed")
    status = gr.Textbox(label="Status")
    gallery = gr.Gallery(label="Captured Images", show_label=True)

    # Logic: Start both stream and saving
    start_btn.click(fn=video_stream_HIKvision,
                    inputs=[rtsp_input, frame_rate_input],
                    outputs=live_frame)

    start_btn.click(fn=start_periodic_image_saving,
                    inputs=[save_interval],
                    outputs=status)
    # Logic: Stop saving
    stop_btn.click(fn=stop_periodic_image_saving,
                   outputs=status)

    # Refresh captured images
    refresh_btn.click(fn=get_recent_images_gallery,
                      outputs=gallery)

demo.launch()
