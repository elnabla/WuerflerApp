import os.path

from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input, Dropout
from keras.models import Sequential

import numpy as np
from sklearn.preprocessing import LabelBinarizer

import backend.constants as c
import random


def binarize(data, classes):
    """

    :param data: 1D np.array
    :param classes: list of numbers, possible values of data
    :return: binarized version
    """
    lb = LabelBinarizer()
    lb.fit(classes)
    return lb.transform(data)


def simple_model(input_shape, n_classes):
    loss = 'categorical_crossentropy'
    if n_classes == 2:
        n_classes = 1
        loss = "binary_crossentropy"
    model = Sequential(
        [
            Input(shape=input_shape),
            Conv2D(32, kernel_size=(3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, kernel_size=(3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dropout(0.5),
            Dense(n_classes, activation="softmax"),
        ]
    )
    model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])
    return model


# start doing stuff
for row in ['P', 'G', 'DG']:
    classes = c.CLASSES_DICT[row]
    n_classes = len(classes)
    X = []
    y = []
    for value in classes:
        data_path = os.path.join(c.DATA_PATH, f"{value}.npz")
        data = np.load(data_path)
        X.append(data['X_data'])
        y.append(data['y_data'])
    X_data = np.concatenate(X, axis=0)
    y_data_raw = np.concatenate(y, axis=0)
    y_data = binarize(y_data_raw, classes)

    # shuffle / Needs to be done because model.fit doesn't shuffle before splitting into train and validation data
    zipped = [e for e in zip(X_data, y_data)]
    random.shuffle(zipped)
    X_data, y_data = zip(*zipped)
    X_data = np.array(X_data)
    y_data = np.array(y_data)
    input_shape = (c.CELL_WIDTH, c.CELL_HEIGHT, 1)
    model = simple_model(input_shape, n_classes)

    model.fit(X_data, y_data, batch_size=32, epochs=30,  validation_split=0.1, shuffle=True)
    model_name = f"simple_model_{row}.h5"
    model.save(os.path.join(c.DATA_PATH, model_name))
