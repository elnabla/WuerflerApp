import cv2
import os

import keras
import albumentations as A
import numpy as np

from helpers import get_augmented

# testing stuff
ones_path = "./roi2/1/"
fours_path = "./roi2/4/"
twos_path = "./roi2/2/"
file = ones_path + os.listdir(ones_path)[0]
image = cv2.imread(file)


transform = A.ShiftScaleRotate(rotate_limit=5, p=1)
aug_image = transform(image=image)['image']
aug_image = cv2.resize(aug_image,  (28, 29))


files = os.listdir(twos_path)
images_twos = []
for file in files:
    file = twos_path + file
    image = cv2.imread(file)
    images_twos.append(get_augmented(image, 100))
images_twos = np.concatenate(images_twos, axis=0)
print(images_twos.shape)

images_fours = []
files = os.listdir(fours_path)
for file in files:
    file = fours_path + file
    image = cv2.imread(file)
    images_fours.append(get_augmented(image, 100))
images_fours = np.concatenate(images_fours, axis=0)
print(images_fours.shape)

X_data = np.concatenate([images_twos, images_fours], axis=0)
X_data = np.expand_dims(X_data, axis=3)
print("data shape", X_data.shape)
# zero is two and 1 is four
y_data = np.array([[1,0]]*3100 + [[1,0]]*3100)
print(y_data.shape)

input_shape = (28, 28, 1)
num_classes = 2

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        keras.layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(num_classes, activation="softmax"),
    ]
)

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(X_data, y_data, batch_size=32, epochs=5,  validation_split=0.1)

model.save('first_model_2_4.h5')
