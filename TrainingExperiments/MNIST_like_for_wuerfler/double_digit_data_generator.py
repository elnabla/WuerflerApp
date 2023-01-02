import random

import matplotlib.pyplot as plt
import tensorflow.keras as tk
import keras
import numpy as np


# inspiration from https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly
class DoubleDigitTrainingDataGenerator(keras.utils.Sequence):
    def __init__(self, batch_size=32, length=100, n_classes=22,
                 possible_numbers=None):
        if possible_numbers is None:
            possible_numbers = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 35, 40, 45, 50, 80]
        self.dim = (28, 28)
        self.batch_size = batch_size
        self.n_channels = 1
        self.length = length
        self.n_classes = n_classes
        self.possible_numbers = possible_numbers
        self.digit_generator = DoubleDigitDataGenerator()

    def __len__(self):
        """
        Denotes the number of batches per epoch. This is given directly in our case
        """
        return self.length

    def __getitem__(self, index):
        """
        Index is not needed, but might be needed by parent class...
        Generate one batch of the data
        """
        # Generate labels
        numbers = random.choices(self.possible_numbers, k=self.batch_size)

        # Generate data
        X = [self.digit_generator.generate_number(number) for number in numbers]
        X = np.array(X)
        X = X.astype('float32') / 255  # normalize to [0, 1] range

        return X, numbers

    def getitem(self, index):
        """
        Index is not needed, but might be needed by parent class...
        Generate one batch of the data
        """
        # Generate labels
        numbers = random.choices(self.possible_numbers, k=index)

        # Generate data
        X = [self.digit_generator.generate_number(number) for number in numbers]
        X = np.array(X)
        X = X.astype('float32') / 255  # normalize to [0, 1] range

        return X, np.array(numbers)


class DoubleDigitDataGenerator:
    def __init__(self):
        (X_train, y_train), (_, _) = tk.datasets.mnist.load_data()
        self.mnist_X = X_train
        self.mnist_y = y_train
        print(X_train.shape)
        print(y_train.shape)


    @staticmethod
    def get_by_label(lst, labels, value):
        extract = []
        for i, val in enumerate(labels):
            if val == value:
                extract.append(lst[i])
        return extract

    def get_random_image_of_digit(self, digit):
        assert digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        images_of_given_digit = self.get_by_label(self.mnist_X, self.mnist_y, digit)
        return random.choice(images_of_given_digit)

    @staticmethod
    def cut(image):
        """
        Takes a 28 by 28 images and gives a 28 by 14 image
        """
        # start = random.randint(5,10)
        start = 7
        stop = start + 14
        return image[:, start:stop]

    @classmethod
    def concatenate_images(cls, image1, image2):
        """
        Concatenate two single digit 28x28 greyscale array to a single 28x28 array
        TODO: manage the overlap better by incorporating stuff from both array
        """
        return np.hstack((cls.cut(image1), cls.cut(image2)))

    def generate_two_digit_number(self, number):
        assert 10 <= number < 100
        first_digit = number // 10
        second_digit = number % 10
        first_image = self.get_random_image_of_digit(first_digit)
        second_image = self.get_random_image_of_digit(second_digit)
        return self.concatenate_images(first_image, second_image)

    def generate_number(self, number):
        assert 0 <= number < 100
        if number < 10:
            return self.get_random_image_of_digit(number)
        return self.generate_two_digit_number(number)

    def plot(self, number):
        plt.imshow(self.generate_number(number), cmap='gray')
        plt.show()


if __name__ == "__main__":
    DoubleDigitDataGenerator().plot(42)
    X, y = DoubleDigitTrainingDataGenerator().getitem__(3)
    print(X.shape)
