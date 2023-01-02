from datetime import datetime
import logging

import cv2
from matplotlib import pyplot as plt
import albumentations as A
import numpy as np
import os
import random
import tensorflow.keras as tk


class DoubleDigitDataGenerator:
    def __init__(self):
        (X_train, y_train), (_, _) = tk.datasets.mnist.load_data()
        self.mnist_X = X_train
        self.mnist_y = y_train
        #print(X_train.shape)
        #print(y_train.shape)

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

    def generate_number_batch(self, number, n):
        images = []
        for i in range(n):
            now = datetime.now()
            logging.warning(f"{now.strftime('%H:%M:%S')} Generate Number {number} #{i}")
            images.append(self.generate_number(number))
        return images

    def plot(self, number):
        plt.imshow(self.generate_number(number), cmap='gray')
        plt.show()


def visualize(image):
    plt.imshow(image, cmap='gray')
    # plt.show() doesn't work


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def visualize(image):
    plt.figure(figsize=(15, 15))
    plt.axis('off')
    plt.imshow(image)


def preprocess(image, resize=True):
    if resize:
        image = cv2.resize(image, (28, 28))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = apply_brightness_contrast(image, 0, 64)
    return 255 - image


def get_augmented(image, number):
    images = []
    transform = A.ShiftScaleRotate(rotate_limit=5, p=1)
    for _ in range(number):
        aug_image = transform(image=image)['image']
        images.append(preprocess(aug_image))
    return np.array(images)


def sliding_window(image, step_width, step_height, ws):
    # slide a window across the image
    print(image.shape[0] - ws[1] + 1)
    for y in range(0, image.shape[0] - ws[1] + 1, step_height):
        for x in range(0, image.shape[1] - ws[0] + 1, step_width):
            # yield the current window
            yield x, y, image[y:y + ws[1], x:x + ws[0]]


def annotate_image(image, im_name,  im_path, height_ratio=1):
    if not os.path.exists(im_path):
        raise FileNotFoundError(f"No such directory: '{im_path}'")

    im_size = image.shape[:2]
    window_height = int(im_size[0] * height_ratio)
    window_width = int(window_height * 50 / 35.0)
    print(window_height, window_width)
    step_witdh = int(window_width / 10.0)
    step_height = int((1-height_ratio)*window_height/3)
    print(step_height)

    for (x, y, roi) in sliding_window(image, step_witdh, step_height, (window_width, window_height)):
        plt.imshow(roi)
        plt.show()
        label = input("Input label: ")
        label = "junk" if label == "" else label
        # results.append([x, y, roi, label])
        path = im_path + f"{label}/im{im_name}_{x}_{y}.png"
        try:
            cv2.imwrite(path, roi)
            print(f"Writing file : '{path}'")
        except:
            print(f"Error writing file: {path}")


def overlay(im1, im2):
    if im1.shape != im2.shape:
        raise ValueError(f"Image shapes not the same: {im1.shape} vs {im2.shape}")
    new = []
    for i in range(im1.shape[0]):
        row = []
        for j in range(im1.shape[1]):
            row.append(max(im1[i,j],im2[i,j]))
        new.append(row)
    return np.array(new)



if __name__ == "__main__":
    image = cv2.imread(f"./images/2022-12-29_blank/im0b.png")
    annotate_image(image, "im2", "./roi_blank/", 0.95)
