import cv2
from box_extractor import BoxExtractor
from cell_extractor import CellExtractor


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
        self.color_image = cv2.imread(self.image_path)
        if self.color_image is None:  # cv2.imread doesn't raise exceptions but return None...
            raise ValueError(f'Could not read image {self.image_path}')

    def _compute_box(self):
        extractor = BoxExtractor(self.image)
        self.box = extractor.extract_box(self.image)

    def _compute_cells(self):
        extractor = CellExtractor(self.box)
        self.cells = extractor.compute_cells()
