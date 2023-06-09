import os
from PIL import Image
from create_dataset import Licenseplates
from sklearn.model_selection import train_test_split
import shutil

def main():

    images_path = 'raw_data/images'
    annotation_path = 'raw_data/annotations'
    labels_path = 'raw_data/labels'

    #create dataset
    dataset = Licenseplates(images_path, annotation_path)

    #create labels for yolo model:
    preprocess_annotations(dataset.data, labels_path)

    #all images and labels as list
    images = [os.path.join(images_path, x) for x in os.listdir(images_path)]
    labels = [os.path.join(labels_path, x) for x in os.listdir(labels_path)]

    images.sort()
    labels.sort()

    #split data into train and test split
    train_imgs, test_imgs, train_labels, test_labels = train_test_split(images, labels, train_size=0.8, random_state=1)

    split_list = [train_imgs, test_imgs, train_labels, test_labels]
    #create folders for train and test splits
    train_img_path = 'yolo_model_data/images/train/'
    test_img_path = 'yolo_model_data/images/test/'
    train_label_path = 'yolo_model_data/labels/train/'
    test_label_path = 'yolo_model_data/labels/test/'

    
    folder_list = [train_img_path, test_img_path, train_label_path, test_label_path]

    for folder in folder_list:
        os.makedirs(folder)
    
    #move the data to the respective folder
    for data,path in zip(split_list, folder_list):
        move_data(data, path)
    
    

#adjust annotations for yolo model and write to .txt files
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


#resize images for yolo model NOT NEEDED 
def preprocess_images(path, resize_path, size=(640, 640)):
 
    for image_path in os.listdir(path):

        if image_path.endswith('.png'):
            
            image_path1 = os.path.join(path, image_path)
            image_path2 = os.path.join(resize_path, image_path)
       
            image = Image.open(image_path1)
            resized_image = image.resize(size)
            resized_image.save(image_path2)

# move images and labels to train and validation folders to upload them to the google colab for training the model
def move_data(file_list, dest_folder):
    for f in file_list:
        try:
            shutil.move(f, dest_folder)
        except:
            print(f)
            assert False


if __name__ == "__main__":
    main()       
