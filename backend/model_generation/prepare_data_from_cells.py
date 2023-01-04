"""
Concatenate data from the cell jpegs. The other method of creating the data did not verify that the boxes
were extracted correctly, leading to completely bad images. It is easy to clean out the mess by erasing the
bad jpegs.
"""

import numpy as np
import os
import cv2
import backend.constants as c


for number in c.CLASSES:
    X_data = []
    y_data = []
    print(number)
    directory = os.path.join(c.CELLS_PATH, str(number))
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        cell = cv2.imread(file_path)
        X_data.append(cell)
        y_data.append(number)  # that is so wrong, ... [number]*n ...
    data_name = f"{number}_checked.npz"
    np.savez(
        os.path.join(c.DATA_PATH, data_name),
        X_data=np.array(X_data),
        y_data=np.array(y_data)
    )
    print(f"Saved data of {len(y_data)} cell images to {data_name}")
