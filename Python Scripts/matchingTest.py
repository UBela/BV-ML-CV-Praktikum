import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_image(img):
    # Load the image
    image = cv2.resize(img, (1280, 1024))

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

    # Apply Gaussian blur to the image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection
    edges = cv2.Canny(blur, 50, 150)

    # Perform a dilation and erosion to close gaps in between object edges
    dilated = cv2.dilate(edges, None, iterations=2)
    eroded = cv2.erode(dilated, None, iterations=1)

    # Find contours in the image
    contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

# Load the two images
img1 = cv2.imread('cam_frames\image_10.JPG')
img2 = cv2.imread('cam_frames\image_11.JPG')

# Process the images to get the contours
contours1 = process_image(img1)
contours2 = process_image(img2)

# Find the largest contour in each image
contour1 = max(contours1, key=cv2.contourArea)
contour2 = max(contours2, key=cv2.contourArea)

# Compute the similarity between the two contours
ret = cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I1, 0.0)

print(f"Match value: {ret}")


# Draw contours onto the images
img1_with_contours = cv2.drawContours(img1.copy(), [contour1], -1, (0, 255, 0), 3)
img2_with_contours = cv2.drawContours(img2.copy(), [contour2], -1, (0, 255, 0), 3)

# Convert color from BGR to RGB
img1_with_contours = cv2.cvtColor(img1_with_contours, cv2.COLOR_BGR2RGB)
img2_with_contours = cv2.cvtColor(img2_with_contours, cv2.COLOR_BGR2RGB)

# Use matplotlib to display the images
plt.figure(figsize=(10, 10))
plt.subplot(1, 2, 1)
plt.imshow(img1_with_contours)
plt.title('Image 1')

plt.subplot(1, 2, 2)
plt.imshow(img2_with_contours)
plt.title('Image 2')

plt.show()
