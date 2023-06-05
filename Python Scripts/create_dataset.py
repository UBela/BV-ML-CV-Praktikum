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
           
            # Use an XML parser to extract relevant information from the XML file
            # and create a dictionary containing image filename, bounding box coordinates, and image dimensions
            # Append the dictionary to the data list
            xml_path = os.path.join(self.annotation_dir, xml_file)
            info = xet.parse(xml_path)
            root = info.getroot()
            image_filename = root.find('filename').text
            image_width = int(root.find('size/width').text)
            image_height = int(root.find('size/height').text)

            annotations = []
            for obj in root.findall('object'):
                label = obj.find('name').text
                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)
                bb = [xmin, ymin, xmax, ymax]
            data.append({
                'filename': image_filename,
                'width': image_width,
                'height': image_height,
                'class': 0,
                'bounding_box': bb
                 })

        return data
