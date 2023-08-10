import cv2
import numpy as np;
import timeit;
import pickle
import binascii



def get_contours(image):
    image = np.array(image)
    image = cv2.resize(image, (1000, 1000))

    # Initialize mask and rectangle
    mask = np.zeros(image.shape[:2], np.uint8)
    rect = (100,200,700,700)  # should be changed according to the image

    # Apply GrabCut
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 3, cv2.GC_INIT_WITH_RECT)

    # Create new mask where sure or likely background is set to 0, otherwise 255
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

    # Multiply original image with new mask to get segmented image
    image = image*mask2[:,:,np.newaxis]

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur the image
    # blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Bilateral Filtering
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)

    _, lp_threshold = cv2.threshold(filtered, 6, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Ensure edges is binary
    _, binary = cv2.threshold(lp_threshold, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort by contour area and keep the largest 10
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

    # Draw contours on the image
    cv2.drawContours(image, contours[0], -1, (0,255,0), 3)

    return contours, image



def compare_contours(image1, image2):

    # Start timer
    start = timeit.default_timer()

    # Get contours of two images
    contours1, image1 = get_contours(image1)
    contours2, image2 = get_contours(image2)

    # Find the largest contour in each image
    contour1 = max(contours1, key=cv2.contourArea)
    contour2 = max(contours2, key=cv2.contourArea)

    # Compute the similarity between the two contours
    ret = cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I1, 0.0)

    print(f"Match value: {ret}")


    # Stop timer
    end = timeit.default_timer()
    # Time elapsed
    print(f"Time taken by get_contours: {end - start} seconds")

    # Concatenate and display images
    combined = np.hstack((image1, image2))
    cv2.imshow('Images with Contours', combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_contour(img):
    contours, _ = get_contours(img)
    print("reached contours")
    # Find the largest contour in the image
    contour = max(contours, key=cv2.contourArea)
    
    contour_pickled = pickle.dumps(contour)

    contour_hex = binascii.hexlify(contour_pickled)
    # Save contour to a file
    with open('contour.pkl', 'wb') as f:
        f.write(contour_hex)

def compare_ContourImage(contour,image):

    # Start timer
    start = timeit.default_timer()

    contoursImg, _ = get_contours(image)
    contourImg = max(contoursImg, key=cv2.contourArea)

    # Compute the similarity between the two contours
    ret = cv2.matchShapes(contourImg, contour, cv2.CONTOURS_MATCH_I1, 0.0)

    # Stop timer
    end = timeit.default_timer()
    # Time elapsed
    print(f"Time taken by compare_ContourImage: {end - start} seconds")

    print(f"Match value: {ret}")

    if (ret < 0.1):
        return True
    else: 
        return False

    
