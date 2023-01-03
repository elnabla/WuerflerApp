"""
Simple cell extractor. Cut a box into cells using predefined cuts, defined by average cell position
This isn't the prettiest since the grids are not the same on the good old sheet...
I want to change Opa's scoring sheet as little as possible.
TODO: factorize code by making CellExtractor an abstract class.
"""

import cv2
import numpy as np

import backend.constants as c


class SimpleCellExtractor:
    P_CUTS_W = [.30, .52, .76, 1]
    P_CUTS_H = [.16, .228, .296, .367, .4375, .503, .573, .644, .709, .78, .848, .921]

    def __init__(self, box):
        self.box = box  # greyscale image
        self.h_cuts = self.get_lines('horizontal')
        self.v_cuts = self.get_lines('vertical')
        self.h_starts = [self.h_cuts[i] for i in range(0, 3)]
        self.h_stops = [self.h_cuts[i] for i in range(1, 4)]
        self.v_starts = [self.v_cuts[i] for i in range(0, 11)]
        self.v_stops = [self.v_cuts[i] for i in range(2, 12)]
        self.cells = None

    def get_lines(self, orientation):
        if orientation == 'horizontal':
            cuts = self.P_CUTS_W
            length = self.box.shape[0]
        elif orientation == 'vertical':
            cuts = self.P_CUTS_H
            length = self.box.shape[1]
        else:
            raise ValueError(f"orientation is not one of 'horizontal or 'vertical': '{orientation}'")
        return [int(cut * length) for cut in cuts]

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

    def get_cell(self, row_letter, col):
        if row_letter not in c.ROWS:
            raise ValueError(f'row_letter must be in {c.ROWS}')
        if col not in [1, 2, 3]:
            raise ValueError(f"col must be in [1, 2, 3]")
        row = c.ROW_DICT[row_letter]
        return self.cells[row, col - 1, :, :]
