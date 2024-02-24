import csv
import cv2
import numpy as np

# Function to load data from CSV
def load_data_from_csv(csv_file):
    data = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)
            for i in range(0, len(lines), 3):
                counter = int(lines[i][0])
                color_image = np.array(lines[i+1], dtype=np.uint8)
                depth_image = np.array(lines[i+2], dtype=np.uint8)
                data.append({'counter': counter, 'color': color_image, 'depth': depth_image})
        return data
    except FileNotFoundError:
        return []

# Function to write data to CSV
def write_to_csv(csv_file, data):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for entry in data:
            writer.writerow([entry['counter']])
            writer.writerow(entry['color'].flatten())
            writer.writerow(entry['depth'].flatten())

# Example usage
csv_file_to_load = 'data1.csv'
loaded_data = load_data_from_csv(csv_file_to_load)

current_index = 0

while True:
    if not loaded_data:
        print("No data to display.")
        break

    entry = loaded_data[current_index]
    counter = entry['counter']
    color_image_loaded = entry['color'].reshape(480, 640, 3)
    depth_image_loaded = entry['depth'].reshape(480, 640)

    cv2.imshow('Loaded Color Image', color_image_loaded)
    cv2.imshow('Loaded Depth Image', depth_image_loaded)

    key = cv2.waitKey(0)
    if key == ord('n'):
        current_index = (current_index + 1) % len(loaded_data)
    elif key == ord('p'):
        current_index = (current_index - 1) % len(loaded_data)
    elif key == ord('d'):
        # Delete the current entry
        loaded_data.pop(current_index)
        print(f'Deleted entry {counter}')

        # Write the updated data back to the CSV file
        write_to_csv(csv_file_to_load, loaded_data)

        current_index = min(current_index, len(loaded_data) - 1)
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
