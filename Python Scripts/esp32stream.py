import cv2

# Replace 'ESP32_CAM_IP' with the actual IP address of your ESP32-CAM
Cam1 = 'http://192.168.178.112:81/stream'
Cam2 = 'http://192.168.178.68:81/stream'

url = Cam1

# Open the video stream
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Failed to open the video stream!")
    exit(1)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    if ret:
        # Display the frame
        cv2.imshow('ESP32-CAM Stream', frame)
    else:
        print("Failed to retrieve frame from the video stream!")

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close windows
cap.release()
cv2.destroyAllWindows()