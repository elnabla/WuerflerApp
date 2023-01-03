import os.path

import cv2

from simple_cell_extractor import SimpleCellExtractor
from box_extractor import BoxExtractor

import matplotlib.pyplot as plt


class CellDetectionPipeline:
    def __init__(self, image_path):
        self.image_path = image_path
        self.color_image = None
        self.image = None
        self.box = None
        self.cells = None

    def run(self):
        self._set_images()
        self._compute_box()
        self._compute_cells()

    def _set_images(self):
        self.color_image = cv2.resize(cv2.imread(self.image_path), (1000, 1500))
        self.image = cv2.cvtColor(self.color_image, cv2.COLOR_BGR2GRAY)
        if self.color_image is None:  # cv2.imread doesn't raise exceptions but return None...
            raise ValueError(f'Could not read image {self.image_path}')

    def _compute_box(self):
        extractor = BoxExtractor(self.image)
        self.box = extractor.extract_box()

    def _compute_cells(self):
        plt.imshow(self.box, cmap='gray')
        plt.show()
        extractor = SimpleCellExtractor(self.box)
        self.cells = extractor.compute_cells()


if __name__ == "__main__":
    path = "../uniform_grids/12.jpg"
    if not os.path.exists(path):
        print("File not found")
    pipeline = CellDetectionPipeline(path)
    pipeline.run()
    print(pipeline.cells.shape)
    plt.imshow(pipeline.box)
    plt.show()
    for j in range(3):
        for i in range(11):
            plt.imshow(pipeline.cells[i, j], cmap='gray')
            plt.show()
