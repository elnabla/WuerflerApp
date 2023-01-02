import cv2
import matplotlib.pyplot as plt

from helpers import sliding_window



import os
print(os.listdir())


for im_number in range(1, 5):
    image = cv2.imread(f"./MNIST_like_for_wuerfler/images/2022-12-28_test/{im_number}.png")
    im_size = image.shape[:2]
    print(im_size)
    window_height = im_size[0]
    window_width = int(window_height * 50 / 35.0)
    print(window_height, window_width)

    for (x, y, roi) in sliding_window(image, 15, 1, (window_width, window_height)):
        plt.imshow(roi)
        plt.show()
        label = input("Input label: ")
        label = "junk" if label == "" else label
        # results.append([x, y, roi, label])
        path = f"./MNIST_like_for_wuerfler/roi_test/{label}/im{im_number}_{x}_{y}.png"
        print(os.listdir(f"./MNIST_like_for_wuerfler/roi_test/{label}/"))
        try: # useless as imwrite does not throw errors...
            cv2.imwrite(path, roi)
        except:
            print(f"Error writing file: {path}")



