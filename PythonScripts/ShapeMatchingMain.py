import matching
import pickle
import cv2
import customtkinter

image_path1 = "PythonScripts\cam_frames\image_11.JPG"
image_path2 = "PythonScripts\cam_frames\image_9.JPG"

image1 = cv2.imread(image_path1, cv2.IMREAD_UNCHANGED)
image2 = cv2.imread(image_path2, cv2.IMREAD_UNCHANGED)

matching.save_contour(image1)

with open('reference_contour.pkl', 'rb') as f:
    contour = pickle.load(f)

print (matching.compare_ContourImage(contour,image2))



