import cv2
import numpy as np


class EdgeOrientator:
    def __init__(self, points):
        self.points = points

    def orient(self):
        quadrants = self.get_quadrants()
        self.reorder_points_according_to_quadrant(quadrants)

    def get_quadrants(self):
        centered_points = self.points - self.points.mean(axis=0)
        quadrants = [self.quadrant(point) for point in centered_points]
        return quadrants

    def reorder_points_according_to_quadrant(self, quadrants):
        indices_of_quadrants_in_order = [quadrants.index(quadrant) for quadrant in [1, 2, 3, 4]]
        self.points = self.points[indices_of_quadrants_in_order]

    @staticmethod
    def quadrant(point):
        x, y = point
        if (x < 0) and (y < 0):
            return 1
        elif (x >= 0) and (y < 0):
            return 2
        elif (x >= 0) and (y >= 0):
            return 3
        else:
            return 4


class GridExtractor:
    def __init__(self, image, points, grid_dims=(500, 750)):
        self.image = image
        self.grid = None
        self.points = points
        self.grid_dims = grid_dims
        self.homography = None

    def extract_grid(self):
        self.compute_homography()
        self.grid = cv2.warpPerspective(self.image, self.homography, self.grid_dims)

    def orient_gridpoints(self):
        orientator = EdgeOrientator(self.points)
        orientator.orient()
        self.points = orientator.points

    def compute_homography(self):
        destination = np.array([[0, 0],
                                [self.grid_dims[0], 0],
                                [self.grid_dims[0], self.grid_dims[1]],
                                [0, self.grid_dims[1]]])
        self.homography, _ = cv2.findHomography(self.points, destination)


class BoxesExtractor(GridExtractor):
    def __init__(self, **kwargs):
        super(BoxesExtractor, self).__init__(**kwargs)
        self.extract_grid()
        self.boxes = None