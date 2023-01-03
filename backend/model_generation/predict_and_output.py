import os

import cv2
import keras.models
import numpy as np
from matplotlib import pyplot as plt

from backend.image_analysis.cell_detection_pipeline import CellDetectionPipeline

path = "../images/test_image.jpg"
if not os.path.exists(path):
    print("File not found")
pipeline = CellDetectionPipeline(path)
pipeline.run()
box = 255 - pipeline.box

model = keras.models.load_model("../data/1_to_5_first_attempt.h5")

def reverse_prediction(lst):
    current_index = 0
    current_max = 0
    for i, value in enumerate(lst):
        if value >= current_max:
            current_index = i
            current_max = value
    return current_index

summe = 0
for j in range(3):
    for i in range(11):
        cell = pipeline.cells[i, j, :, :]
        print(cell.shape)
        pred = model.predict(np.array([cell]))[0]
        value = reverse_prediction(pred)
        summe += value
        print(reverse_prediction(pred), pred)
        cv2.putText(
            box,  # numpy array on which text is written
            f"{value}",  # text
            (j*50 + 80, i*28 + 80),  # position at which writing has to start
            cv2.FONT_HERSHEY_SIMPLEX,  # font family
            0.8,  # font size
            (0, 0, 0, 255),  # font color
            3)
cv2.putText(
            box,  # numpy array on which text is written
            f"Total: {summe}",  # text
            (30, 380 ),  # position at which writing has to start
            cv2.FONT_HERSHEY_SIMPLEX,  # font family
            0.8,  # font size
            (0, 0, 0, 255),  # font color
            3)
plt.imshow(box, cmap='gray')
plt.show()