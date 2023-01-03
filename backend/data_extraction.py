import os

import cv2
import numpy as np

import constants as c
import select_grid

import pickle


def extract_training_data_from_images():
    array = get_all_data()
    save_training_data(array)


def read_training_data_from_binary(filename):
    file_path = os.path.join(c.DATA_DIR, f'training_data_{c.TRAINING_IMAGES_VERSION}.pickle')
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


def save_training_data(array):
    file_path = os.path.join(c.DATA_DIR, f'training_data_{c.TRAINING_IMAGES_VERSION}.pickle')
    with open(file_path, 'wb') as file:
        pickle.dump(array, file)


def get_all_data() -> dict:
    data = {}
    for class_type in c.CLASSES:
        data[class_type] = get_data_from_class(class_type)
    return data


def get_data_from_class(class_type) -> np.array:
    images_folder = _get_folders_dict()[class_type]
    image_list = os.listdir(images_folder)
    data = []
    print(class_type)
    for image_name in image_list:
        print(image_name)
        image = cv2.imread(os.path.join(images_folder, image_name))
        cells = select_grid.get_cells_from_image(image)
        flattened_cells = flatten_cells(cells)
        data.append(flattened_cells)
    return np.array(data)


def flatten_cells(cells):
    data = []
    for class_type in range(11):
        for col in [0, 1, 2]:
            data.append(cells[class_type][col])
    return np.array(data).reshape((33, c.CELL_WIDTH, c.CELL_HEIGHT))


def _get_folders_dict() -> dict:
    folders = {}
    for class_type in c.CLASSES:
        folders[class_type] = os.path.join(c.IMAGE_DIR, str(class_type))
    return folders


if __name__ == '__main__':
    extract_training_data_from_images()





