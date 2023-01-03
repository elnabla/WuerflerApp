"""
First little experiment with partial data. About 350 cells for each type.
Validation accuracy of 99% after 10 epochs.
"""

from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential

import numpy as np
import backend.constants as c
import random

GRIDS_PATH = "../images/grids/"
CELLS_PATH = "../images/cells/"
TO_EXTRACT = [0, 1, 2, 3]
N_CLASSES = len(TO_EXTRACT)
DATA_NAME = "0_to_3_first_data.npz"

data = np.load(DATA_NAME)
X_data = data['X_data']
y_data_raw = data['y_data']

categorical_dict = {0: [1, 0, 0, 0], 1: [0, 1, 0, 0], 2: [0, 0, 1, 0], 3: [0, 0, 0, 1]}
y_data = [categorical_dict[y] for y in y_data_raw]

# shuffle
zipped = [e for e in zip(X_data, y_data)]
random.shuffle(zipped)
X_data, y_data = zip(*zipped)
X_data = np.array(X_data)
y_data = np.array(y_data)


input_shape = (c.CELL_WIDTH, c.CELL_HEIGHT, 1)
model = Sequential(
    [
        Conv2D(64, (3, 3), input_shape=input_shape, padding='same', activation='relu'),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Flatten(),
        Dense(4096, activation='relu'),
        Dense(4096, activation='relu'),
        Dense(1000, activation='relu'),
        Dense(N_CLASSES, activation='sigmoid')
    ]
)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_data, y_data, batch_size=32, epochs=10,  validation_split=0.1, shuffle=True)

model.save('1_to_3_first_attempt.h5')
