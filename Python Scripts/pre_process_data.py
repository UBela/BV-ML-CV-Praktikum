import os
from PIL import Image
from create_dataset import Licenseplates
#adjust annotations for yolo mdoel and write to .txt files
def preprocess_annotations(data, save_folder):
    for annotation in data:
        image_width = annotation['width']
        image_height = annotation['height']
        base_filename = os.path.splitext(annotation['filename'])[0]
        save_path = os.path.join(save_folder, base_filename + '.txt')
        with open(save_path, 'w') as f:  # Clear the file before writing annotations
            for bbox_annotation in annotation['annotations']:
                xmin, ymin, xmax, ymax = bbox_annotation['bounding_box']
                x_center = (xmin + xmax) / (2.0 * image_width)
                y_center = (ymin + ymax) / (2.0 * image_height)
                bbox_width = (xmax - xmin) / image_width
                bbox_height = (ymax - ymin) / image_height

                annotation_str = f"{0} {x_center} {y_center} {bbox_width} {bbox_height}"

                f.write(annotation_str + '\n')


#resize images for yolo model
def preprocess_images(path, resize_path, size=(640, 640)):
 
    for image_path in os.listdir(path):
        if image_path.endswith('.png'):
            
            image_path1 = os.path.join(path, image_path)
          
            image_path2 = os.path.join(resize_path, image_path)
       
            image = Image.open(image_path1)
            resized_image = image.resize(size)
            resized_image.save(image_path2)

