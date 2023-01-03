import cv2
import matplotlib.cm as cm
import matplotlib.pyplot as plt

import constants as c


def imshow_grey(img):
    plt.imshow(img, cmap=cm.Greys_r)


def extract_gridpoints(img):
    clean = clean_image(img)
    gridpoints = locate_gridpoints(clean)
    n = len(gridpoints)

    if n != 4:
        raise GridNotFoundException(f'Did not find 4 gridpoints. Found {n}')

    gridpoints = gridpoints.reshape((n, 2))
    return reorder_gridpoints(gridpoints)




def plot_point(img, point, number):
    return cv2.putText(img, f"{number}",
                       (point[0], point[1]),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       5, (255, 0, 0), 30, 2)


def plot_points(img, points):
    for i in range(len(points)):
        img = plot_point(img, points[i, :], i + 1)
    return img








def slice_box_horizontally(stripe, lines, lengths):
    starts = [lines[i] + lengths[i] for i in range(len(lines) - 1)]
    stops = lines[1:]
    return [stripe[:, (start + 1):(stop - 1)] for start, stop in zip(starts, stops)]


def slice_box_vertically(box, lines, lengths):
    starts = [lines[i] + lengths[i] for i in range(len(lines) - 1)]
    stops = lines[1:]
    return [box[(start + 1):(stop - 1), :] for start, stop in zip(starts, stops)]


def slice_box_given_separators(box, h_separators, v_separators):
    # take only cells which are filled with numbers
    h_lines = h_separators[0][1:]
    h_lengths = h_separators[1][1:]
    v_lines = v_separators[0][2:14]
    v_lengths = v_separators[1][2:14]
    return [
        [cv2.resize(cell, (c.CELL_WIDTH, c.CELL_HEIGHT)) for cell in slice_box_vertically(slice, v_lines, v_lengths)]
        for slice in slice_box_horizontally(box, h_lines, h_lengths)]


def slice_box(box):
    h_separators = correct_h_lines(get_h_lines(box))
    v_separators = correct_v_lines(get_v_lines(box))
    return slice_box_given_separators(box, h_separators, v_separators)


def get_cells_from_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    points = extract_gridpoints(image)
    box = transform_grid(image, points)
    return slice_box(box)


class Junk:
    @staticmethod
    def _get_image(image_path):
        image = cv2.imread(image_path)
        if image in None:
            raise ImageNotReadableError(f'{image_path} could not be read as an image')
        return image

    def extract_cells(self):
        points = self.extract_gridpoints()
        self.box = self.get_box(points)
        self.cells = self.get_cells











if __name__ == "__main__":
    image_path = 'data/test_images/im8.jpg'
    image = cv2.imread(image_path)

    extractor = BoxExtractor(image)
    extractor.preprocess_image()
    extractor.locate_grid_points()
    print(extractor.points)

