import cv2
import numpy as np

import backend.constants as c
from edge_orientator import EdgeOrientator


class BoxExtractor:
    def __init__(self, image):
        self.image = image
        self.processed_image = None
        self.points = None
        self.homography = None

    def extract_box(self, image_to_transform):
        """There are different images we might want to use for the extraction:
        the raw_image, and various transformations thereof
        It depends on the usage. Keep ip open for now"""
        assert (image_to_transform.shape == self.image.shape)
        self.preprocess_image()
        self.locate_gridpoints()
        self.orient_gridpoints()
        self.compute_homography()
        box = cv2.warpPerspective(image_to_transform, self.homography, (c.BOX_WIDTH, c.BOX_HEIGHT))
        return box

    def preprocess_image(self):
        # Todo: remove magic numbers
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        kernel_big = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))

        grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (11, 11), 0)
        close = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.adaptiveThreshold(close, 255, 0, 1, 19, 2)
        self.processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_big)

    def locate_gridpoints(self):
        _, contours, _ = cv2.findContours(self.processed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Contour with biggest area
        contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        perimeter = cv2.arcLength(contour, True)
        points = cv2.approxPolyDP(contour, 0.05 * perimeter, True)

        n_points = len(points)
        if n_points != 4:
            raise GridNotFoundException(f"Found {n_points} instead of 4  :-(")

        points = points.reshape((4, 2))
        self.points = points

    def orient_gridpoints(self):
        orientator = EdgeOrientator(self.points)
        orientator.orient()
        self.points = orientator.points

    def compute_homography(self):
        destination = np.array([[0, 0], [c.BOX_WIDTH, 0], [c.BOX_WIDTH, c.BOX_HEIGHT], [0, c.BOX_HEIGHT]])
        h, _ = cv2.findHomography(self.points, destination)
        self.homography = h


class GridNotFoundException(Exception):
    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(GridNotFoundException, self).__init__(arg1)

