import random
import tensorflow.keras as tk
import keras
import numpy as np
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tk.datasets.mnist.load_data()


def my_plot(array):
    plt.imshow(array, cmap='gray')


def get_by_label(lst, labels, value):
    extract = []
    for i, val in enumerate(labels):
        if val == value:
            extract.append(lst[i])
    return extract


def get_random_image_of_digit(digit):
    assert digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    images_of_given_digit = get_by_label(x_train, y_train, digit)
    return random.choice(images_of_given_digit)


def cut(image):
    """
    Takes a 28 by 28 images and gives a 28 by 14 image
    """
    # start = random.randint(5,10)
    start = 7
    stop = start + 14
    return image[:, start:stop]


def concatenate(image1, image2):
    """
    Concatenate two single digit 28x28 greyscale array to a single 28x28 array
    TODO: manage the overlap better by incorporating stuff from both array
    """
    return np.hstack((cut(image1), cut(image2)))


def concatenate_random(images):
    return concatenate(random.choice(images), random.choice(images))


def concatenate_plot(images):
    my_plot(concatenate_random(images))


def generate_two_digit_number(number):
    assert 10 <= number < 100
    first_digit = number // 10
    second_digit = number % 10
    first_image = get_random_image_of_digit(first_digit)
    second_image = get_random_image_of_digit(second_digit)
    return concatenate(first_image, second_image)


def generate_number(number):
    assert 0 <= number < 100
    if number < 10:
        return get_random_image_of_digit(number)
    return generate_two_digit_number(number)


possible_numbers = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 35, 40, 45, 50, 80]

if __name__ == "__main__":
    my_plot(generate_number(42))
    plt.show()

