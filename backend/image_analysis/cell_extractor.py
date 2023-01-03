import cv2
import numpy as np

import backend.constants as c
from line_detector import HorizontalLineDetector, VerticalLineDetector
from backend.exceptions import LinesNotFoundError


class CellExtractor:
    def __init__(self, box):
        self.box = box
        self.h_lines = self.safely_get_lines('horizontal')
        self.v_lines = self.safely_get_lines('vertical')
        self.h_starts = self.get_h_starts()
        self.h_stops = self.get_h_stops()
        self.v_starts = self.get_v_starts()
        self.v_stops = self.get_v_stops()
        self.cells = None

    def safely_get_lines(self, orientation):
        if orientation == 'vertical':
            detector = VerticalLineDetector(self.box)
        elif orientation == 'horizontal':
            detector = HorizontalLineDetector(self.box)
        else:
            raise ValueError

        try:
            lines = detector.get_lines()
        except LinesNotFoundError as e:
            #  lines = self.get_lines_manually(orientation)  # TODO: implement this manual fallback?
            raise e
        return lines

    def get_h_starts(self):
        return [self.h_lines[i][1] for i in range(1, 4)]

    def get_h_stops(self):
        return [self.h_lines[i][0] for i in range(2, 5)]

    def get_v_starts(self):
        return [self.v_lines[i][1] for i in range(2, 13)]

    def get_v_stops(self):
        return [self.v_lines[i][0] for i in range(3, 14)]

    def compute_cells(self):
        cells = []
        for v_start, v_stop in zip(self.v_starts, self.v_stops):
            for h_start, h_stop in zip(self.h_starts, self.h_stops):
                cell = self.box[v_start:v_stop, h_start:h_stop]
                cell = cv2.resize(cell, (c.CELL_WIDTH, c.CELL_HEIGHT))
                cells.append(cell)
        cells = np.array(cells)
        cells = cells.reshape((11, 3, c.CELL_WIDTH, c.CELL_HEIGHT))
        self.cells = cells


