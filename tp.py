





import numpy as np
import streamlit as st
import cv2
# Function to create VideoCapture objects for each camera
def create_video_captures(urls):
    return [cv2.VideoCapture(url) for url in urls]

# Function to release VideoCaptures
def release_video_captures(caps):
    for cap in caps:
        cap.release()

# Function to display live video streams in Streamlit
def display_video_streams(caps, num_cameras):
    st.title("Multi-Camera Video Stream")

    # Create a placeholder for the video streams
    video_placeholders = [st.empty() for _ in range(num_cameras)]

    # Get the video frame width and height from the first camera
    frame_width = int(caps[0].get(3))
    frame_height = int(caps[0].get(4))

    # Define the codec and create a VideoWriter object for each camera
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like MJPG, XVID, etc.
    outs = [cv2.VideoWriter(f'output_camera_{i + 1}.avi', fourcc, 20.0, (frame_width, frame_height)) for i in range(len(caps))]

    while True:
        frames = [cap.read()[1] for cap in caps]  # Read frames from all cameras

        # Write the combined frame to the output video file for each camera
        for i, out in enumerate(outs):
            out.write(frames[i])

        # Display live video streams
        for i, frame in enumerate(frames):
            video_placeholders[i].image(frame, channels="BGR", width=frame_width)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    # Release the VideoWriters and VideoCaptures
    for out in outs:
        out.release()

    release_video_captures(caps)

# Streamlit app
def main():
    st.sidebar.title("Multi-Camera Video Stream Configuration")
    num_cameras = st.sidebar.number_input("Enter the number of cameras:", min_value=1, max_value=10, step=1)
    urls = [st.sidebar.text_input(f"Enter the URL for camera {i + 1}:") for i in range(num_cameras)]

    if st.sidebar.button("Start Video Stream"):
        caps = create_video_captures(urls)
        display_video_streams(caps, num_cameras)

if __name__ == "__main__":
    main()
