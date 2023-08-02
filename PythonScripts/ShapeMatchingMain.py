import matching
import pickle
import customtkinter
from UI import App

matching.save_contour("PythonScripts\cam_frames\image_11.JPG")

with open('reference_contour.pkl', 'rb') as f:
    contour = pickle.load(f)

matching.compare_ContourImage(contour,"PythonScripts\cam_frames\image_9.JPG")

app_instance = App(customtkinter.CTk)

app_instance.run()



