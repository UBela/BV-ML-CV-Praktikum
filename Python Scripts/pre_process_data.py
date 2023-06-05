import os
from PIL import Image

#adjust annotations for yolo mdoel and write to .txt files
def preprocess_annotations(data, save_folder):
    # Create the save folder if it doesn't exist
   

    for annotation in data:
        # Get image width and height
        image_width = annotation['width']
        image_height = annotation['height']

        # Get bounding box coordinates
        xmin, ymin, xmax, ymax = annotation['bounding_box']

        # Calculate YOLO coordinates
        x_center = (xmin + xmax) / (2.0 * image_width)
        y_center = (ymin + ymax) / (2.0 * image_height)
        bbox_width = (xmax - xmin) / image_width
        bbox_height = (ymax - ymin) / image_height

        # Format annotation as a string
        annotation_str = f"0 {x_center} {y_center} {bbox_width} {bbox_height}"

        # Save annotation as a text file
        base_filename = os.path.splitext(annotation['filename'])[0]
        
        save_path = os.path.join(save_folder, base_filename + '.txt')

        with open(save_path, 'w') as f:
            f.write(annotation_str)

#resize images for yolo model
def preprocess_images(path, size=(640, 640)):
    
    for image_path in os.listdir(path):
        if image_path.endswith('.png'):
            
            image_path = os.path.join(path, image_path)
            image = Image.open(image_path)
            resized_image = image.resize(size)
            resized_image.save(image_path)