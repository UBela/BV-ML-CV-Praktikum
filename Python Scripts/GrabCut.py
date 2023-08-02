import cv2
import numpy as np

# Read the image
image = cv2.imread('cam_frames/image_8.jpg')

# Create a mask initialized with zeros
mask = np.zeros(image.shape[:2], np.uint8)

# Define the foreground and background models
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

x = 300  # x-coordinate of the top-left corner
y = 200  # y-coordinate of the top-left corner
width = 900   # Width of the rectangle
height = 700  # Height of the rectangle


# Define the rectangular region enclosing the car (adjust as per your needs)
rect = (x, y, width, height)  # Replace x, y, width, height with appropriate values

# Apply GrabCut segmentation
cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# Create a mask where the background pixels are marked as 0 and the foreground pixels as 1 or 3
mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Apply the mask to the original image
segmented_image = image * mask[:, :, np.newaxis]

# Convert the segmented image to grayscale
gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred, 30, 150)

# Display the segmented image and the edges
cv2.imshow('Segmented Image', segmented_image)
cv2.imshow('Edges', edges)
cv2.imwrite('edges_image.jpg', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
