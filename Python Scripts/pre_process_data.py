from create_dataset import Licenseplates
import torch
from torch.utils.data import  DataLoader
from torchvision import transforms

path_images = './data/images/'
path_annotations = './data/annotations/'

dataset = Licenseplates(path_images, path_annotations)


#Pre-Processing the images:
images = []
annotations = []

# Split dataset into images and annotations
for image, annotation in dataset:
    images.append(image)
    annotations.append(annotation)

transformations = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((416, 416)),  
])


def preprocess_images(images, transform=transformations):

  transformed_images = [transform(image) for image in images]
  transformed_images = torch.stack(transformed_images) 

  #normalize the images    
  transformed_images = transformed_images.float() / 255.
  mu, std = transformed_images.mean(dim=(0,2,3)), transformed_images.std((0,2,3))

  normalize = transforms.Normalize(mean=mu, std=std)
  transformed_images = [normalize(image) for image in transformed_images]
  return torch.stack(transformed_images)

def preprocess_annotations(annotations):
    transformed_annotations = []
    for annotation in annotations:
        # Perform preprocessing operations on the annotation
        id = 0
        xmin, ymin, xmax, ymax = annotation['bounding_box']
        w = annotation['width']
        h =  annotation['height']
        x_center = (xmin + xmax) / (2.0 * w)
        y_center = (ymin + ymax) / (2.0 * h)
        bbox_width = (xmax - xmin) / w
        bbox_height = (ymax - ymin) / h
        transformed_annotations.append([x_center, y_center, bbox_width, bbox_height,int(id)])

        
    return torch.tensor(transformed_annotations)