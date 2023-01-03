"""
First little experiment with partial data. About 350 cells for each type.
Validation accuracy of 99% after 10 epochs.
"""
import os.path

from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input, Dropout
from keras.models import Sequential

import numpy as np
import backend.constants as c
import random

TO_EXTRACT = [0, 1, 2, 3, 4, 5]
N_CLASSES = len(TO_EXTRACT)

X_data = []
y_data_raw = []
for value in TO_EXTRACT:
    data_path = os.path.join(c.DATA_PATH, f"{value}.npz")
    data = np.load(data_path)

    X_data.append(data['X_data'])
    y_data_raw.append(data['y_data'])
X_data = np.concatenate(X_data, axis=0)
y_data_raw = np.concatenate(y_data_raw, axis=0)
categorical_dict = {0: [1, 0, 0, 0, 0, 0],
                    1: [0, 1, 0, 0, 0, 0],
                    2: [0, 0, 1, 0, 0, 0],
                    3: [0, 0, 0, 1, 0, 0],
                    4: [0, 0, 0, 0, 1, 0],
                    5: [0, 0, 0, 0, 0, 1]
                    }
y_data = [categorical_dict[y] for y in y_data_raw]

# shuffle / Needs to be done because model.fit doesn't shuffle before splitting into train and validation data
zipped = [e for e in zip(X_data, y_data)]
random.shuffle(zipped)
X_data, y_data = zip(*zipped)
X_data = np.array(X_data)
y_data = np.array(y_data)


input_shape = (c.CELL_WIDTH, c.CELL_HEIGHT, 1)
model = Sequential(
    [
        Input(shape=input_shape),
        Conv2D(32, kernel_size=(3, 3), activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, kernel_size=(3, 3), activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dropout(0.5),
        Dense(N_CLASSES, activation="softmax"),
    ]
)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_data, y_data, batch_size=32, epochs=50,  validation_split=0.1, shuffle=True)

model.save(os.path.join(c.DATA_PATH, '1_to_5_first_attempt.h5'))
