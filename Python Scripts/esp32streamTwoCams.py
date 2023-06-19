import cv2

# Replace 'ESP32_CAM_IP' with the actual IP address of yo ur ESP32-CAM
Cam1 = 'http://192.168.178.112:81/stream'
Cam2 = 'http://192.168.178.68:81/stream'

# Open the video stream
cap1 = cv2.VideoCapture(Cam1)
cap2 = cv2.VideoCapture(Cam2)

if not cap1.isOpened():
    print("Failed to open the video stream!")
    exit(1)

while True:
    # Read a frame from the video stream
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if ret1:

        #frame1_resized = cv2.resize(frame1, (1280, 1024))
        #frame2_resized = cv2.resize(frame2, (1280, 1024))

        frame_combined = cv2.hconcat([frame1, frame2])
        #frame_combined = cv2.hconcat([frame1_resized, frame2_resized])

        cv2.imshow('ESP32-CAM Stream', frame_combined)
    else:
        print("Failed to retrieve frame from the video stream!")

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close windows
cap1.release()
cap2.release()
cv2.destroyAllWindows()