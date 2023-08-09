import time
from ultralytics import YOLO
import numpy as np
import os
import cv2
# import pytesseract
import torch
from PIL import Image
import imutils
import easyocr
import torchvision

print(torch.__version__)
print(torchvision.__version__)

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# ocr reader
reader = easyocr.Reader(['de'])
pattern = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÜÖ'

# trained yolo model
lp_detect_model = YOLO("finalfinal/yolo_model/best.pt")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
lp_detect_model.to(device)


def process_license_plates(path_to_cam_frames):
    img_files = [os.path.join(path_to_cam_frames, f) for f in os.listdir(path_to_cam_frames)
                if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')]
   
    all_lp_ids= list(map(find_license_plate_id, img_files))
    all_lp_ids = np.array(all_lp_ids).flatten().tolist()
    predicted_license_plate_id = max(set(all_lp_ids), key=all_lp_ids.count)
    predicted_license_plate_id = predicted_license_plate_id.replace(" ","")
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

def apply_image_processing(img):
    kernel = np.ones((3,3),np.uint8) #1
  
    lp_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lp_gray = cv2.erode(lp_gray, kernel, iterations=1)
    lp_gray = cv2.bilateralFilter(lp_gray, 5, 75, 75)
    _, lp_threshold = cv2.threshold(lp_gray, 6, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return lp_threshold

def pls_work(license_plate, name='test'):
    img_g = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
    img = cv2.bilateralFilter(img_g, 11, 17, 17)
    img = cv2.threshold(img, 6, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    """
    keypoints = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    max_c = max(contours, key=cv2.contourArea)
    max_c = cv2.approxPolyDP(max_c, 20, True)
    mask = np.zeros(img_g.shape, np.uint8)
    new_image = cv2.drawContours(mask, [max_c], 0,255, -1)

    new_image = np.where(mask == 255, img_g, 0)
    #rotated_img = warp_image(img, max_c)
    #TODO Sunday: maybe use minarearectangle to descew
    masked_img_gray = cv2.bilateralFilter(new_image, 3,32,32)
    masked_img_gray = cv2.threshold(masked_img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #masked_img_gray = cv2.Canny(masked_img_gray, 30, 200)
    cv2.imwrite("test_results/masked_"+name, new_image)
    cv2.imwrite("test_results/processed_"+name, masked_img_gray)
    """
    return img       
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
    if detected_licenseplates is None:
            return "No License Plate Detected!"
    pre_processed = pls_work(detected_licenseplates)
    #re_cropped = preprocess_license_plate(detected_licenseplates, img_file.split("/")[-1])
    
    lp_text = reader.readtext(pre_processed, allowlist= pattern,detail=0,paragraph=True)
    if lp_text:
        return lp_text
    return "License Plate Text not detected"

if __name__ == '__main__':
    path_to_cam_frames = 'finalfinal/test images 5.8/SHGLF206/sharp'
    id, img = process_license_plates(path_to_cam_frames)
    print(id)