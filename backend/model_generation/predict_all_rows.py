import os

import cv2
import keras.models
import numpy as np
import backend.constants as c
from matplotlib import pyplot as plt

from backend.image_analysis.cell_detection_pipeline import CellDetectionPipeline

path = "../images/test_image_2.jpg"
if not os.path.exists(path):
    print("File not found")
pipeline = CellDetectionPipeline(path)
pipeline.run()
box = 255 - pipeline.box
box = cv2.resize(box, (400, 800))
box = cv2.cvtColor(box, cv2.COLOR_GRAY2BGR)



def reverse_prediction(lst, classes):
    if len(classes) == 2:
        # binary classification
        if lst > 0.5:
            return classes[1]
        else:
            return classes[0]
    # multiclass case
    current_index = 0
    current_max = 0
    for i, value in enumerate(lst):
        if value >= current_max:
            current_index = i
            current_max = value
    return classes[current_index]

summe = 0
for i, row in enumerate(c.ROWS) :
    print(row, ' is being processed')
    path_to_model = os.path.join(c.DATA_PATH, f"simple_model_{row}.h5")
    model = keras.models.load_model(path_to_model)
    cells = pipeline.cells[i, :, :, :]
    preds = model.predict(cells)
    for j, pred in enumerate(preds):
        value = reverse_prediction(pred, c.CLASSES_DICT[row])
        summe += value
        cv2.putText(box, f"{value}", (2*(j*48 + 60), 2*(i*28 + 75)), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0, 255), 3)
cv2.putText(
            box,  # numpy array on which text is written
            f"Total: {summe}",  # text
            (2*30, 2*390 ),  # position at which writing has to start
            cv2.FONT_HERSHEY_SIMPLEX,  # font family
            0.8,  # font size
            (255, 0, 0, 255),  # font color
            3)
plt.imshow(box, cmap='gray')
plt.show()