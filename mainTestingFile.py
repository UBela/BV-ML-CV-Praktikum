from PythonScripts import matching
from UI_Folder import UI
import customtkinter
import pickle

app_instance = UI.App()

app_instance.mainloop()

app_instance.upload_image_to_database("TestImagesSet1\image_1.jpg", True, "SHG-FF-206")

matching.save_contour("PythonScripts\cam_frames\image_11.JPG")

with open('reference_contour.pkl', 'rb') as f:
    contour = pickle.load(f)

matching.compare_ContourImage(contour,"PythonScripts\cam_frames\image_9.JPG")
