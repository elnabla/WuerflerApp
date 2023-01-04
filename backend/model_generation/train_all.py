import os.path

from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input, Dropout
from keras.models import Sequential

import numpy as np
from sklearn.preprocessing import LabelBinarizer

import backend.constants as c
import random


SELECTED_MODEL_NAME = 'simple'
MODEL_SUFFIX = '2'


def binarize(data, classes):
    """

    :param data: 1D np.array
    :param classes: list of numbers, possible values of data
    :return: binarized version
    """
    lb = LabelBinarizer()
    lb.fit(classes)
    return lb.transform(data)


def get_model(name, input_shape, n_classes):
    if name == 'simple':
        return simple_model(input_shape, n_classes)
    if name == 'vgg':
        return vgg_model(input_shape, n_classes)
    raise ValueError(f"{name} not one of 'simple' or 'vgg'")


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


def vgg_model(input_shape, n_classes):

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
            Dense(n_classes, activation='sigmoid')
        ]
    )
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# start doing stuff
for row in c.ROWS:
    print(f'Training row:  {row}')
    classes = c.CLASSES_DICT[row]
    n_classes = len(classes)
    X = []
    y = []
    for value in classes:
        data_path = os.path.join(c.DATA_PATH, f"{value}_checked.npz")
        data = np.load(data_path)
        X.append(data['X_data'])
        y.append(data['y_data'])
    X_data = np.concatenate(X, axis=0)
    y_data_raw = np.concatenate(y, axis=0)
    print('DIMS: ', X_data.shape)
    y_data = binarize(y_data_raw, classes)

    # shuffle / Needs to be done because model.fit doesn't shuffle before splitting into train and validation data
    zipped = [e for e in zip(X_data, y_data)]
    random.shuffle(zipped)
    X_data, y_data = zip(*zipped)
    X_data = np.array(X_data)
    y_data = np.array(y_data)
    input_shape = (c.CELL_WIDTH, c.CELL_HEIGHT, 1)
    model = get_model(SELECTED_MODEL_NAME, input_shape, n_classes)

    model.fit(X_data, y_data, batch_size=32, epochs=40,  validation_split=0.1, shuffle=True)
    model_name = f"{SELECTED_MODEL_NAME}_model_{MODEL_SUFFIX}_{row}.h5"
    model.save(os.path.join(c.DATA_PATH, model_name))
