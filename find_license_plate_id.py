from ultralytics import YOLO
import numpy as np
import os
import cv2
import pytesseract
import torch
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#trained yolo model
lp_detect_model = YOLO('yolo_model/best.pt')

device = 'cuda' if torch.cuda.is_available() else 'cpu'

lp_detect_model.to(device)

def main():
    start = time.time()
    path_to_cam_frames = 'cam_frames'
    all_lp_ids = []
    img_files = [os.path.join(path_to_cam_frames, f) for f in os.listdir(path_to_cam_frames)
                if f.endswith('.jpg') or f.endswith('.png')]
    all_lp_ids = map(find_license_plate_id, img_files)
    all_lp_ids = [lp_id for lp_id in all_lp_ids if lp_id is not None]
    predicted_license_plate_id = max(set(all_lp_ids), key=all_lp_ids.count)
    print(predicted_license_plate_id)
    end = time.time()
    print(f"Time: {np.round(end - start, 2)}")



#crop the license plate and save as image
def crop_license_plates(img, yolo_model, save_img=False):
    img_name = img.split("\\")[-1]
    
    detected_lps = yolo_model.predict(img, verbose=False)[0]
    license_plates = []
    
    for lp in detected_lps.boxes.data.tolist():
        
        x1, y1, x2, y2, conf, _ = lp
        
        img_array = cv2.imread(img)
        cropped_lp =img_array[int(y1):int(y2), int(x1):int(x2), :]
        license_plates.append(cropped_lp)
        if save_img:
            cv2.imwrite(f"cropped_license_plates/cropped_{img_name}", cropped_lp)
        
    return license_plates

def ocr(image):
    custom_config = r'--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZÖ0123456789'
    text = pytesseract.image_to_string(image, lang='deu', config=custom_config)
    if text:
        return text.strip("\n")
    return "not detected"

def apply_image_processing(img):
    kernel = np.ones((3,3),np.uint8)
    # grayscale
    lp_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # erosion
    lp_gray = cv2.erode(lp_gray, kernel, iterations=1)
    # bilateral filter
    lp_gray = cv2.bilateralFilter(lp_gray, 5, 75, 75)
    # binary thresholding
    _, lp_threshold = cv2.threshold(lp_gray, 6, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return lp_threshold


def preprocess_license_plate(license_plate, name, save_img=False):
    
    lp_threshold = apply_image_processing(license_plate)
    
    contours, _ = cv2.findContours(lp_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # contour with largest area
    max_contour = max(contours, key=cv2.contourArea)
    #warped_img = warp_image(license_plate.copy(), max_contour)
    
    # Crop the license plate region
    x, y, w, h = cv2.boundingRect(max_contour)
    license_plate_cropped = lp_threshold[y:y + h, x:x + w]

    if save_img:
        cv2.imwrite(f'thresholded_license_plates/thresh_bil_rectified_{name}', license_plate_cropped)

    return license_plate_cropped

def find_license_plate_id(img_file):

    detected_licenseplates = crop_license_plates(img_file, lp_detect_model)
    assert len(detected_licenseplates) == 1, "WARNING! More than one License plate detected. Access denied!"
    re_cropped = preprocess_license_plate(detected_licenseplates[0], img_file, save_img=False)
    if re_cropped is not None:
        return ocr(re_cropped)
    return "not detected"

if __name__ == '__main__':
    main()

