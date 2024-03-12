!pip install opencv-python
import cv2
import numpy as np

# Get the number of cameras from the user
num_cameras = int(input("Enter the number of cameras: "))

# Collect URLs for each camera from the user
urls = []
for i in range(num_cameras):
    url = input(f"Enter the URL for camera {i + 1}: ")
    urls.append(url)

# Create VideoCapture objects for each camera
caps = [cv2.VideoCapture(url) for url in urls]

# Check if all video captures are successfully opened
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"Error: Unable to open video stream for camera {i + 1}.")
        exit()

# Get the video frame width and height from the first camera
frame_width = int(caps[0].get(3))
frame_height = int(caps[0].get(4))

# Define the codec and create a VideoWriter object for each camera
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can use other codecs like MJPG, XVID, etc.
outs = [cv2.VideoWriter(f'output_camera_{i + 1}.avi', fourcc, 20.0, (frame_width, frame_height)) for i in range(len(caps))]

# Create a named window with normal size
cv2.namedWindow('Grid', cv2.WINDOW_NORMAL)

while True:
    frames = [cap.read()[1] for cap in caps]  # Read frames from all cameras

    # Arrange frames in a grid based on the number of cameras
    grid_rows = int(np.ceil(num_cameras / 2))
    grid_cols = min(2, num_cameras)
    grid = []
    for r in range(grid_rows):
        row_frames = frames[r * grid_cols: (r + 1) * grid_cols]
        row = np.hstack(row_frames)
        grid.append(row)

    combined_frame = np.vstack(grid)

    cv2.imshow('Grid', combined_frame)

    # Write the combined frame to the output video file for each camera
    for i, out in enumerate(outs):
        out.write(frames[i])

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release the VideoWriters and VideoCaptures
for out in outs:
    out.release()

for cap in caps:
    cap.release()

# Close the named window
cv2.destroyAllWindows()
