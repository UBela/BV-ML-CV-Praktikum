import matching
import pickle
import cv2
import customtkinter

image_path1 = "finalfinal/test images 5.8/SHGLF206/sharp/test (1).jpg"
image_path2 = "finalfinal/test images 5.8/SHGLF206/sharp/test (2).jpg"

image1 = cv2.imread(image_path1, cv2.IMREAD_UNCHANGED)
image2 = cv2.imread(image_path2, cv2.IMREAD_UNCHANGED)

matching.save_contour(image1)

with open('reference_contour.pkl', 'rb') as f:
    contour = pickle.load(f)

print (matching.compare_ContourImage(contour,image2))



