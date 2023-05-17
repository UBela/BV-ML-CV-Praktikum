import cv2
import time

def capture_images_from_esp32_cam(ip_address, capture_count):
    url = f'http://{ip_address}/stream'

    # Open the video stream
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("Failed to open the video stream!")
        return

    # Set the resolution for the captured images
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

    # Capture and save the images
    for i in range(capture_count):
        ret, frame = cap.read()

        if ret:
            image_name = f"image_{i+1}.jpg"
            cv2.imwrite(image_name, frame)
            print(f"Image {i+1} captured and saved as {image_name}")
            time.sleep(.5)
        else:
            print(f"Failed to capture image {i+1}")

    # Release the video stream
    cap.release()

# Usage example
ip_address = "192.168.178.112:81"  # Replace with the actual IP address of your ESP32-CAM
capture_count = 2

capture_images_from_esp32_cam(ip_address, capture_count)