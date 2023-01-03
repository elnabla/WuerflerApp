import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, 'data', 'training_images')
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'training_data')
TEST_DIR = os.path.join(ROOT_DIR, 'data', 'test_images')


# box extraction
BOX_WIDTH = 200
BOX_HEIGHT = 400

CELL_HEIGHT = 28
CELL_WIDTH = 28

ROWS = [1, 2, 3, 4, 5, 6, 'S', 'F', 'G', 'DG']
CLASSES = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 35, 40, 45, 50, 80]

TRAINING_IMAGES_VERSION = 0
