import matching
import pickle
import customtkinter

matching.save_contour("PythonScripts\cam_frames\image_11.JPG")

with open('reference_contour.pkl', 'rb') as f:
    contour = pickle.load(f)

matching.compare_ContourImage(contour,"PythonScripts\cam_frames\image_9.JPG")



