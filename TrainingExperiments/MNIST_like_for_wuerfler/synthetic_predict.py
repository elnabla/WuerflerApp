import cv2
import os

import keras
import matplotlib.pyplot as plt
import numpy as np

from helpers import preprocess

possible_numbers = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24,  25, 30, 35, 40, 45, 50, 80]
#possible_numbers = [1, 5, 15]



# testing stuff
ones_path = "./roi2/1/"
fours_path = "./roi2/4/"
twos_path = "./roi2/2/"
print(os.listdir(twos_path))

path = ones_path
images = []
for file in os.listdir(path):
    print(file)
    file = path + file
    image = cv2.imread(file)
    image = preprocess(image, resize=False)
    image = cv2.resize(image, (50, 35))
    image = image.astype('float') / 255
    images.append(image)
    #plt.imshow(image)
    #plt.show()
print(images[:2])
images = np.array(images)

model = keras.models.load_model("synth_model_22_10000.h5")
preds = model.predict(np.array(images))

for pred in preds:

    # Initialize variables to keep track of the maximum element and its index
    max_element = float('-inf')  # minimum float value
    max_index = 0

    # Use the enumerate function to iterate over the elements and their indices
    for i, element in enumerate(pred):
      # If the current element is greater than the maximum element, update the maximum element and its index
      if element > max_element:
        max_element = element
        max_index = i

    print(max_index, possible_numbers[max_index])  # Output: 3 (the index of the maximum element, which is 5)