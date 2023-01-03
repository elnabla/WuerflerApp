import cv2
import numpy as np

import backend.constants as c
from backend.image_analysis.edge_orientator import EdgeOrientator
from backend.exceptions import BoxNotFoundException


class BoxExtractor:
    def __init__(self, image):
        self.image = cv2.resize(image, (1000, 1500))
        self.processed_image = None
        self.points = None
        self.homography = None

    def extract_box(self):
        # assert (image_to_transform.shape == self.image.shape)
        self.preprocess_image()
        self.locate_grid_points()
        self.orient_grid_points()
        self.compute_homography()
        return cv2.warpPerspective(self.processed_image, self.homography, (c.BOX_WIDTH, c.BOX_HEIGHT))

    def preprocess_image(self):
        # Todo: remove magic numbers
        # grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # https://stackoverflow.com/questions/44047819/increase-image-brightness-without-overflow/44054699#44054699
        # compute an approximate background image in order to remove shadows
        dilated_img = cv2.dilate(self.image, np.ones((15, 15), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(self.image, bg_img)
        norm_img = diff_img.copy()
        norm_img = cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        # denoise and binarize
        grey = cv2.fastNlMeansDenoising(norm_img, None, 20, 7, 21)
        grey = cv2.GaussianBlur(grey, (7, 7), 0)
        self.processed_image = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY_INV, 11, 2)

    def locate_grid_points(self):
        # further process the image: dilate to close some gaps in the grid
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
        dilated = cv2.dilate(self.processed_image, kernel, 5)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Contour with the biggest area
        # TODO: be smarter about this ? check contourArea in certain range ?
        contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        self.points = self.approximate(contour)

    @staticmethod
    def approximate(contour):
        perimeter = cv2.arcLength(contour, True)
        for coef in [.03, .04, .05, .06, .07, .08, .09, .1]:
            approximation = cv2.approxPolyDP(contour, coef * perimeter, True)
            n = len(approximation)
            print(coef, n)
            if n == 4:
                break
        if n != 4:
            raise BoxNotFoundException(f"Found {n} edge points instead of 4  :-(")
        return approximation.reshape((n, 2))

    def orient_grid_points(self):
        orientator = EdgeOrientator(self.points)
        orientator.orient()
        self.points = orientator.points

    def compute_homography(self):
        destination = np.array([[0, 0], [c.BOX_WIDTH, 0], [c.BOX_WIDTH, c.BOX_HEIGHT], [0, c.BOX_HEIGHT]])
        h, _ = cv2.findHomography(self.points, destination)
        self.homography = h


