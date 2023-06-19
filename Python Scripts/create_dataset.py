import os
from PIL import Image
from torch.utils.data import Dataset
import xml.etree.ElementTree as xet

class Licenseplates(Dataset):

    def __init__(self, image_dir, annotation_dir):
        self.image_dir = image_dir
        self.annotation_dir = annotation_dir
        self.data = self._parse_xml_files()
       
  
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image_path = os.path.join(self.image_dir, self.data[idx]['filename'])
        image = Image.open(image_path).convert("RGB")

        annotations = self.data[idx]

        # Return image and annotations as tensors
        return image, annotations

    def _parse_xml_files(self):
        # Parse XML files and extract relevant information
        data = []
        xml_files = [file for file in os.listdir(self.annotation_dir) if file.endswith('.xml')]
        
        for xml_file in xml_files:
            label_dict = {}
            xml_path = os.path.join(self.annotation_dir, xml_file)
            info = xet.parse(xml_path).getroot()
            image_filename = info.find('filename').text
            image_width = int(info.find('size/width').text)
            image_height = int(info.find('size/height').text)

            annotations = []
            for obj in info.findall('object'):
                label = obj.find('name').text
                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)
                bbox = [xmin, ymin, xmax, ymax]
                
                annotations.append({
                    'class': label,
                    'bounding_box': bbox
                })

            data.append({
                'filename': image_filename,
                'width': image_width,
                'height': image_height,
                'annotations': annotations
            })

        return data