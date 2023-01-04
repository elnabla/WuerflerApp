"""
Create a bunch of 28*28 images of cells based on photographs of grids filled with the same number.
Starting with X, 1, 2, 3, 4 and 5. Because it is slow to fill out those sheets.
Also extract empty cells in the hope of creating synthetic data
"""

import numpy as np
import os
import cv2
import backend.constants as c

from backend.image_analysis.cell_detection_pipeline import CellDetectionPipeline
from backend.exceptions import BoxNotFoundException


TO_EXTRACT = [16]


for content in TO_EXTRACT:
    X_data = []
    y_data = []
    path_to_images = os.path.join(c.GRIDS_PATH, f"{content}")
    path_to_cells = os.path.join(c.CELLS_PATH, f"{content}")
    print(path_to_images, 'contains: ')
    print(os.listdir(path_to_images))
    for file_name in os.listdir(path_to_images):
        path = os.path.join(path_to_images, file_name)
        pipeline = CellDetectionPipeline(path)
        try:
            pipeline.run()
            for j in range(3):
                for i in range(11):
                    cell = pipeline.cells[i, j]
                    cell_file_name = f"{i}_{j}_" + file_name
                    cell_file_path = os.path.join(path_to_cells, cell_file_name)
                    # print("Saving " + cell_file_path)
                    cv2.imwrite(cell_file_path, cell)
                    X_data.append(cell)
                    y_data.append(content)
            print(f'Could extract file {path}')
        except BoxNotFoundException:
            print(f"Couln't extract file: {path}")
    data_name = f"{content}.npz"
    data_path = os.path.join(c.DATA_PATH, data_name)
    print("Saving data to file:" + data_path)
    np.savez(data_path, X_data=np.array(X_data), y_data=np.array(y_data))
