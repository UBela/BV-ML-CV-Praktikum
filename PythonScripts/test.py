import pre_process_data


#create dataset
path_images = '../data/images/'
path_annotations = '/data/annotations/'
resize_path = '../data/resized_images'
pre_process_data.preprocess_images(path_images, resize_path)
