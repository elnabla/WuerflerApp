from abc import ABC, abstractmethod

import numpy as np

import helpers

from backend.exceptions import LinesNotFoundError


class LineDetector(ABC):
    def __init__(self, box):
        self.box = box
        self.box_width = box.shape[1]
        self.box_height = box.shape[0]

        # to be set by deriving class
        self.stripe_length = None
        self.expected_line_count = None
        self.type = 'abstract'

    def get_lines(self):
        stripe = self.get_stripe()
        binarized_stripe = self.binarize(stripe)
        lines = self.binary_to_lines(binarized_stripe)
        return self.clean_lines(lines)

    @abstractmethod
    def get_stripe(self):
        pass

    def binarize(self, stripe):
        """ A stripe has peaks corresponding to the black lines, those are marked as True
        We must make the baseline level, and compute a threshold to set pixels to black/white"""
        background = helpers.running_median(stripe, self.get_stride())  # gives the level of the ground white
        diff = np.abs(stripe - background)  # base line white is now level
        thresh = self.compute_binarization_threshold(diff)
        binarized_stripe = [s > thresh for s in diff]
        return binarized_stripe

    @staticmethod
    def compute_binarization_threshold(diff):
        return max(5 * np.percentile(np.sort(diff), 85), 10)  # at least 10 for when percentile is 0: lot of pure white

    def get_stride(self):
        stride = int(self.box_height / 40)
        if stride % 2 == 0:
            stride += 1
        return stride

    @classmethod
    def binary_to_lines(cls, binarized):
        starts = []
        stops = []
        current_line = False
        for i, is_black in enumerate(binarized):
            if cls.line_starts(is_black, current_line):
                starts.append(i)
                current_line = True
            elif cls.line_stopped(is_black, current_line):
                stops.append(i - 1)
                current_line = False
        if current_line:  # unfinished black line at the end
            stops.append(len(binarized))
        lines = list(zip(starts, stops))
        return lines

    @staticmethod
    def line_starts(is_black, current_line):
        return is_black and not current_line

    @staticmethod
    def line_stopped(is_black, current_line):
        return not is_black and current_line

    def clean_lines(self, lines):
        if self.last_line_not_at_edge(lines):
            lines.append((self.stripe_length, self.stripe_length))  # add at the edge of box
        if self.first_line_not_at_edge(lines):
            lines.insert(0, (0, 0))  # add fictive first line
        if len(lines) != self.expected_line_count:
            msg = f"{self.type} line count should be {self.expected_line_count}, " + \
                f"found {len(lines)} instead: {lines}"
            raise LinesNotFoundError(msg)
        return lines

    def last_line_not_at_edge(self, lines):
        return lines[-1][0] < self.stripe_length * (self.expected_line_count - 1.5) / (self.expected_line_count - 1)

    def first_line_not_at_edge(self, lines):
        return lines[0][1] > self.stripe_length * 0.5 / (self.expected_line_count - 1)


class HorizontalLineDetector(LineDetector):
    def __init__(self, box):
        super().__init__(box)
        self.stripe_length = self.box_width
        self.expected_line_count = 5
        self.type = 'horizontal'

    def get_stripe(self):
        # get slice of the last row that should always be empty as a 1D array
        # magic numbers based on shape of the box (rows always identically spaced)
        start = int(self.box_height / 40 * 37.5)
        stop = int(self.box_height / 40 * 39.5)
        stripe = self.box[start:stop, :].mean(axis=0)
        return stripe


class VerticalLineDetector(LineDetector):
    def __init__(self, box):
        super().__init__(box)
        self.stripe_length = self.box_height
        self.expected_line_count = 15
        self.type = 'vertical'

    def get_stripe(self):
        # get a slice of the first column of the box, before the categories (1,2,3, ...,  S, F, P...)
        # magic numbers based on average shape of the box (spacing of columns varies)
        start = int(self.box_width / 40)
        stop = start * 2
        stripe = self.box[:, start:stop].mean(axis=1)
        return stripe
