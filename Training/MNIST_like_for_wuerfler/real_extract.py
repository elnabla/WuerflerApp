import json
import os
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt

from extractor import GridExtractor
from helpers import sliding_window

i=1

im_dir = "./images/uniform_grids/"
ann_path = im_dir + f"{i}.json"  # dirty
with open(ann_path) as file:
    data = json.load(file)
pts = data['shapes'][0]['points']
print(pts)
im_path = im_dir + data['imagePath'].split('/')[-1]
image = cv2.imread(im_path)

pts = np.array(pts, np.int32)
pts = pts.reshape((-1, 1, 2))
print(pts)
image = cv2.polylines(image, np.int32([pts]), True,  (255, 0, 0), thickness=50)
plt.imshow(image)
plt.show()

grid = GridExtractor(image, pts, [500, 750]).extract_box()
plt.imshow(grid)
plt.show()

true_box_height = int(grid.shape[0] / 11.0)
true_box_width = int(grid.shape[1] / 3.0)
extra = int(grid.shape[1]/100)

print(true_box_width, extra)
print(true_box_height, extra)

starts_height = [0] + [true_box_height*i - extra for i in range(1, 11)]
ends_height = [true_box_height*i + extra for i in range(1, 11)] + [grid.shape[0]]
print(zip(starts_height, ends_height))


starts_width = [0] + [true_box_width*i - extra for i in range(1, 3)]
ends_width = [true_box_width*i + extra for i in range(1, 3)] + [grid.shape[1]]
print(zip(starts_width, ends_width))

for x_start, x_end in zip(starts_width, ends_width):
    print("X", [x_start, x_end])
    for y_start, y_end in zip(starts_height, ends_height):
        print(" Y", [y_start, y_end])
        box = grid[y_start:y_end, x_start:x_end]  # cv2 and numpy don't agree on dimensions
        plt.imshow(box)
        plt.show()
        pts = [[x_start, y_start],
               [x_end, y_start],
               [x_end, y_end],
               [x_start, y_end]]
        print(pts)
        color = (0, random.randint(0, 255), random.randint(0, 255))
        #grid = cv2.polylines(grid, np.int32([pts]), True, color, thickness=20)
plt.imshow(grid)
plt.show()





