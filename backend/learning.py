import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import constants as c


class WuerflerNets:
    def __init__(self):
        self.choices = {
            '1': [0, 1, 2, 3, 4, 5],  # 0 is the 'X' mark
            '2': [0, 2, 4, 6, 8, 10],
            '3': [0, 3, 6, 9, 12, 15],
            '4': [0, 4, 8, 12, 16, 20],
            '5': [0, 5, 10, 15, 20, 25],
            '6': [0, 6, 12, 18, 24, 30],
            'S': [0, 20, 25, 30],
            'F': [0, 30, 35],
            'P': [0, 40, 45],
            'G': [0, 50],
            'DG': [0, 80]
        }
        self.models = self.initialize_models()

    def initialize_models(self):
        models = {}
        for key in self.choices.keys:
            models[key] = self.vgg_model(len(self.choices[key]))
        return models

    def train(self, test=False):
        for key in self.choices.keys:
            self.train_key(key, test)

    def train_key(self, key,  test):
        X = []
        y = []
        X_test = None
        y_test = None
        for value in self.choices[key]:
            X_value = self.load_training_data(key)
            y_value = np.repeat(value, len(X_value))
            X.append(X_value)
            y.append(y_value)
        X, y = shuffle(X, y)
        if test:
            X, y, X_value, X_test = train_test_split(X, y, test_size=0.15)
        self.models[key].fit(X, y, epochs=10, batch_size=32)
        if test:
            score = self.models[key].evaluate(X_test, y_test, batch_size=32)
            print(f'    Key: {key:>2}, Test accuracy: {score}')

    @staticmethod
    def vgg_model(n_classes):
        input_shape = (c.CELL_WIDTH, c.CELL_HEIGHT, 1)

        model = Sequential()
        model.Add(Conv2D(64, (3, 3), input_shape=input_shape, padding='same', activation='relu'))
        model.Add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        model.Add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.Add(Conv2D(128, (3, 3), activation='relu', padding='same'))
        model.Add(Conv2D(128, (3, 3), activation='relu', padding='same'))
        model.Add(Conv2D(128, (3, 3), activation='relu', padding='same'))
        model.Add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.Add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        model.Add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        model.Add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        model.Add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.Add(Flatten()),
        model.Add(Dense(4096, activation='relu'))
        model.Add(Dense(4096, activation='relu'))
        model.Add(Dense(1000, activation='relu'))
        model.Add(Dense(n_classes, activation='sigmoid'))
        model.compile(optimizer='adam', loss='categorical_crossentropy', metris=['accuracy'])
        return model
