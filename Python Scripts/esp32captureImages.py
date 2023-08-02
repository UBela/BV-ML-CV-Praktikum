import cv2
import time
import os
IP_ADDRESS = "192.168.178.68:81"
IMAGE_WIDTH = 1600
IMAGE_HEIGHT = 1200

image_path = 'cam_frames/'

if not os.path.exists(image_path):
    os.makedirs(image_path)

def capture_images_from_esp32_cam(ip_address, capture_count):
    url = f'http://{ip_address}:81/stream'

    # Open the video stream
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("Failed to open the video stream!")
        return

    # Set the resolution for the captured images
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

    # Capture and save the images
    for i in range(capture_count):

        ret, frame = cap.read()

        if ret:
            image_name = f"image_{i+1}.jpg"
            cv2.imwrite(image_path + image_name, frame)
            print(f"Image {i+1} captured and saved as {image_name}")
            time.sleep(.5)
        else:
            print(f"Failed to capture image {i+1}")

    # Release the video stream
    cap.release()

capture_images_from_esp32_cam(IP_ADDRESS, 5)