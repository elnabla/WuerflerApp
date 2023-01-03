import cv2
import numpy as np

import backend.constants as c
from edge_orientator import EdgeOrientator


class BoxExtractor:
    def __init__(self, image):
        self.image = cv2.resize(image, (1000, 1500))
        self.processed_image = None
        self.points = None
        self.homography = None

    def extract_box(self, image_to_transform):
        """
        There are different images we might want to use for the extraction:
        the raw_image, and various transformations thereof
        It depends on the usage. Keep ip open for now
        """
        assert (image_to_transform.shape == self.image.shape)
        self.preprocess_image()
        self.locate_gridpoints()
        self.orient_gridpoints()
        self.compute_homography()
        box = cv2.warpPerspective(image_to_transform, self.homography, (c.BOX_WIDTH, c.BOX_HEIGHT))
        return box

    def preprocess_image(self):
        # Todo: remove magic numbers
        #grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        grey = cv2.fastNlMeansDenoising(self.image, None, 20, 7, 21)
        grey = cv2.GaussianBlur(grey, (7, 7), 0)
        self.processed_image = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    def locate_gridpoints(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        thresh2 = cv2.dilate(self.processed_image, kernel, 2)
        contours, _ = cv2.findContours(self.processed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Contour with the biggest area
        contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        perimeter = cv2.arcLength(contour, True)
        points = cv2.approxPolyDP(contour, 0.05 * perimeter, True)

        n_points = len(points)
        if n_points != 4:
            raise GridNotFoundException(f"Found {n_points} grid points instead of 4  :-(")

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

