"""
Create a bunch of 28*28 images of cells based on photographs of grids filled with the same number.
Starting with X, 1, 2 and 3. Because it is slow to fill out those sheets.
Also extract empty cells in the hope of creating synthetic data.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import backend.constants as c
from backend.image_analysis.cell_detection_pipeline import CellDetectionPipeline
from backend.exceptions import BoxNotFoundException

GRIDS_PATH = "../images/grids/"
CELLS_PATH = "../images/cells/"
TO_EXTRACT = [0, 1, 2, 3]
DATA_NAME = "0_to_3_first_data.npz"

X_data = []
y_data = []
for content in TO_EXTRACT:
    path_to_images = GRIDS_PATH + f"{content}/"
    path_to_cells = CELLS_PATH + f"{content}/"
    print(path_to_images, 'contains: ')
    print(os.listdir(path_to_images))
    for file_name in os.listdir(path_to_images):
        path = path_to_images + file_name
        pipeline = CellDetectionPipeline(path)
        try:
            pipeline.run()
            for j in range(3):
                for i in range(11):
                    cell = pipeline.cells[i, j]
                    cell_file_name = f"{i}_{j}_" + file_name
                    cell_file_path = path_to_cells + cell_file_name
                    print("Saving " + cell_file_path)
                    cv2.imwrite(cell_file_path, cell)
                    X_data.append(cell)
                    y_data.append(content)
        except BoxNotFoundException:
            pass


print("Saving data to file:" + DATA_NAME)
np.savez(DATA_NAME, X_data=X_data, y_data=y_data)

