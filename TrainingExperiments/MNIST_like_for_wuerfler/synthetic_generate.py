from synthetize import synth_images
import numpy as np
import os

print(os.listdir())

BLANKS_PATH = "./roi_blank/b/"

possible_numbers = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24,  25, 30, 35, 40, 45, 50, 80]
#possible_numbers = [1, 5, 15]

number_to_classes = {}
classes_to_number = {}
n_classes = len(possible_numbers)
for i, number  in enumerate(possible_numbers):
    class_element = [0]*n_classes
    class_element[i] = 1
    number_to_classes[number] = class_element
    classes_to_number[tuple(class_element)] = number  # list in not hashable so not appropriate, hence tuple

n_per_class = 10000

images = []
labels = []
for number in possible_numbers:
    print(f"[INFO] Starting for number {number}")
    images.append(synth_images(number, BLANKS_PATH, n_per_class))
    for i in range(n_per_class):
        labels.append(number_to_classes[number])

images = np.array(images)
labels = np.array(labels)

np.savez(f"synth_data_{n_classes}_{n_per_class}.npz", X_data=images, y_data=labels)
print(images.shape, labels.shape)
print(labels)
