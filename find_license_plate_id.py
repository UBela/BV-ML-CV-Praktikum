import time
from ultralytics import YOLO
import numpy as np
import os
import cv2
import pytesseract
import torch
from PIL import Image
from io import BytesIO
import pickle

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#trained yolo model
lp_detect_model = YOLO('yolo_model/best.pt')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
lp_detect_model.to(device)

def process_license_plates(path_to_cam_frames):
    img_files = [os.path.join(path_to_cam_frames, f) for f in os.listdir(path_to_cam_frames)
                if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')]
    print(img_files)
    all_lp_ids= list(map(find_license_plate_id, img_files))
    print(all_lp_ids)
    predicted_license_plate_id = max(set(all_lp_ids), key=all_lp_ids.count)
  
    with open(img_files[0], 'rb') as img_file:
        image_data = img_file.read()
    
    return predicted_license_plate_id, image_data    

#crop the license plate and save as image
def detect_license_plate(img, yolo_model, save_img=True):

    img_name = img.split("/")[-1]
    
    detected_lps = yolo_model.predict(img, verbose=False)[0]
    license_plates = []
    
    for lp in detected_lps.boxes.data.tolist():
        
        x1, y1, x2, y2, conf, _ = lp
        
        img_array = cv2.imread(img)
        cropped_lp =img_array[int(y1):int(y2), int(x1):int(x2), :]
        license_plates.append(cropped_lp)
   
    assert len(license_plates) == 1, "WARNING! More than one License plate detected. Access denied!"
    if save_img:
        
        cv2.imwrite(f'cropped_license_plates/cropped_{img_name}', license_plates[0])    
    return license_plates[0]

def ocr(image):

    custom_config = r'--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZÖ0123456789'
    text = pytesseract.image_to_string(image, lang='deu', config=custom_config)
    if text:

        return text.strip("\n")
    return "not detected"

def apply_image_processing(img):
    kernel = np.ones((3,3),np.uint8) #1
    target_width, target_height = 300, 100  # Set your desired maximum target width and height

    # Calculate the aspect ratio of the original license plate image
    original_height, original_width, _ = img.shape
    aspect_ratio = original_width / original_height

    # Determine the new width and height while maintaining the aspect ratio
    if original_width > target_width or original_height > target_height:
        if aspect_ratio >= 3:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)

        # Resize the license plate image to the new dimensions
        img = cv2.resize(img, (new_width, new_height))
    else:
        # Keep the original size if it is within the target dimensions
        img = img.copy()
    # Resize the license plate image to the new dimensions
    
    lp_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lp_gray = cv2.erode(lp_gray, kernel, iterations=1)
    lp_gray = cv2.bilateralFilter(lp_gray, 5, 75, 75)
    _, lp_threshold = cv2.threshold(lp_gray, 6, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return lp_threshold

        
def preprocess_license_plate(license_plate, name, save_img=True):
    
    lp_threshold = apply_image_processing(license_plate)
    cv2.imwrite(f'thresholded_license_plates/processed_{name}', lp_threshold)
    contours, _ = cv2.findContours(lp_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # contour with largest area
    max_contour = max(contours, key=cv2.contourArea)
  
    # Crop the license plate region
    x, y, w, h = cv2.boundingRect(max_contour)
    license_plate_cropped = lp_threshold[y:y + h, x:x + w]

    if save_img:
        cv2.imwrite(f'thresholded_license_plates/crop_processed_{name}', license_plate_cropped)

    return license_plate_cropped

def find_license_plate_id(img_file):
   
    detected_licenseplates = detect_license_plate(img_file, lp_detect_model)
    re_cropped = preprocess_license_plate(detected_licenseplates, img_file.split("/")[-1])
    
    if re_cropped is not None:
        return ocr(re_cropped)
    
    return "not detected"

path_to_cam_frames = 'Python Scripts/cam_frames/'
process_license_plates(path_to_cam_frames)