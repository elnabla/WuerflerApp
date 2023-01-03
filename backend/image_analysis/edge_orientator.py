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
