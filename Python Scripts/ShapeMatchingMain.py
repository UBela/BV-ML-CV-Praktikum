import matching
import pickle

matching.save_contour("cam_frames\image_11.JPG")

with open('reference_contour.pkl', 'rb') as f:
    contour = pickle.load(f)

matching.compare_ContourImage(contour,"cam_frames\image_9.JPG")

matching.compare_contours()