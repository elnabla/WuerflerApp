import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, 'data', 'training_images')
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'training_data')
TEST_DIR = os.path.join(ROOT_DIR, 'data', 'test_images')

GRIDS_PATH = os.path.join(ROOT_DIR, "images", "grids")
CELLS_PATH = os.path.join(ROOT_DIR, "images", "cells")
DATA_PATH = os.path.join(ROOT_DIR, "data")



# box extraction
BOX_WIDTH = 200
BOX_HEIGHT = 400

CELL_HEIGHT = 28
CELL_WIDTH = 28

ROWS = [1, 2, 3, 4, 5, 6, 'S', 'F', 'P', 'G', 'DG']
ROW_DICT = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 'S': 6, 'F': 7, 'P': 8, 'G': 9, 'DG': 10}
CLASSES = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 35, 40, 45, 50, 80]
CLASSES_DICT = {
    1: [0, 1, 2, 3, 4, 5],
    2: [0, 2, 4, 6, 8, 10],
    3: [0, 3, 6, 9, 12, 15],
    4: [0, 4, 8, 12, 16, 20],
    5: [0, 5, 10, 15, 20, 25],
    6: [0, 6, 12, 18, 24, 30],
    'S': [0, 20, 25, 30],
    'F': [0, 30, 35],
    'P': [0, 40, 45],
    'G': [0, 1, 50], # add ones to avoid binary classification, there is a bug for now
    'DG': [0, 1, 80]
}



TRAINING_IMAGES_VERSION = 0

