import cv2
import numpy as np
import pyrealsense2 as rs
import csv

# Initialize Intel RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

# Initialize CSV file for database
csv_file = 'data1.csv'

# Function to write data to CSV
def write_to_csv(csv_file, color_image, depth_image, counter):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([counter])
        writer.writerow(color_image.flatten())
        writer.writerow(depth_image.flatten())

# Function to get the last counter value from CSV
def get_last_counter(csv_file):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)
            if len(lines) > 0:
                return int(lines[-3][0]) + 1
    except FileNotFoundError:
        return 1

# Initialize counter
counter = get_last_counter(csv_file)

# Continuously capture and save data
try:
    while True:
        # Wait for the next set of frames
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        # Convert frames to NumPy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # Display the frames (you can customize this part based on your needs)
        cv2.imshow('Color Frame', color_image)
        cv2.imshow('Depth Frame', depth_image)

        # Check for the key press ('q' to quit, 's' to save)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save data to CSV
            write_to_csv(csv_file, color_image, depth_image, counter)
            counter += 1
            print(f'Data saved to {csv_file}')

finally:
    # Stop the pipeline on exit
    pipeline.stop()
    cv2.destroyAllWindows()
