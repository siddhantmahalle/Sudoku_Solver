import operator

import cv2
import numpy as np

from sudoku_extractor.utils import *
from config import constants


class Extract:
    def __init__(self, img):
        self.image_grid = None
        self.digits = None
        self.squares = None
        self.img = img
        self.length_digits = img.shape[:1][0] / 9

    def get_image_grid(self):
        self.squares = self._get_digit_corners()
        self.digits = self._get_digits()
        self.image_grid = self._create_grid()
        return self.image_grid

    def _get_digit_corners(self):
        squares = []
        for j in range(9):
            for i in range(9):
                point1 = (i * self.length_digits, j * self.length_digits)
                point2 = ((i + 1) * self.length_digits, (j + 1) * self.length_digits)
                squares.append((point1, point2))

        return squares

    def _get_digits(self):
        digits = []
        img = get_preprocessed_image(self.img.copy(), get_dilated_img=False)

        for square in self.squares:
            digits.append(self._extract_digits(img, square, constants.DIGIT_IMAGE_SIZE))

        return digits

    def _extract_digits(self, img, square, size):
        digit = self._get_rect(img, square)
        height, width = digit.shape[:2]

        assumed_pos = int(np.mean([height, width]) / 2.5)

        img_digit, bbox, seed = self._get_digit_bbox(digit, [assumed_pos, assumed_pos],
                                                     [width - assumed_pos, height - assumed_pos])

        # print(bbox)

        width = bbox[1][0] - bbox[0][0]
        height = bbox[1][1] - bbox[0][1]

        if width > 0 and height > 0 and (width * height) > 200 and len(digit) > 0:
            extracted_digit = self._scale_and_centre(digit, constants.DIGIT_IMAGE_SIZE, constants.DIGIT_IMAGE_MARGIN,
                                                     constants.DIGIT_IMAGE_BACKGROUND)
            return extracted_digit
        else:
            extracted_digit = np.zeros((size, size), np.uint8)
            return extracted_digit

    def _get_rect(self, img, square):

        return img[int(square[0][1]):int(square[1][1]), int(square[0][0]):int(square[1][0])]

    def _get_digit_bbox(self, digit, point_1, point_2):

        img = digit.copy()
        height, width = img.shape[:2]

        seed_points = (None, None)
        largest_area = 0

        top_left = [0, 0] if (point_1 is None) else point_1
        bottom_right = [width, height] if (point_2 is None) else point_2

        for x in range(top_left[0], bottom_right[0]):
            for y in range(top_left[1], bottom_right[1]):
                if img.item(y, x) == 255 and x < width and y < height:
                    area = cv2.floodFill(img, None, (x, y), 64)
                    if area[0] > largest_area:
                        largest_area = area[0]
                        seed_points = (x, y)

        for x in range(width):
            for y in range(height):
                if img.item(y, x) == 255 and x < width and y < height:
                    cv2.floodFill(img, None, (x, y), 64)

        mask_floodfill = np.zeros((height + 2, width + 2), np.uint8)

        if all([point is not None for point in seed_points]):
            cv2.floodFill(img, mask_floodfill, seed_points, 255)

        top, bottom, left, right = 0, height, 0, width

        for x in range(width):
            for y in range(height):
                if img.item(y, x) == 64:
                    cv2.floodFill(img, mask_floodfill, (x, y), 0)

                if img.item(y, x) == 255:
                    top = y if y < top else top
                    bottom = y if y > bottom else bottom
                    left = x if x < left else left
                    right = x if x > right else right

        bbox = [[top, left], [right, bottom]]

        return img, np.array(bbox, dtype='float32'), seed_points

    def _scale_and_centre(self, img, size, margin=0, background=0):
        height, width = img.shape[:2]

        if height > width:
            top_pad, bottom_pad, right_pad, left_pad = self._get_border(height, width, size, margin, True)
        else:
            top_pad, bottom_pad, right_pad, left_pad = self._get_border(height, width, size, margin, False)

        img = cv2.resize(img, (width, height))
        img = cv2.copyMakeBorder(img, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_REFLECT, None, background)
        img = cv2.resize(img, (size, size))
        return img

    def _get_border(self, height, width, size, margin, is_height_greater: bool):

        b1 = int(margin / 2)
        b2 = b1
        ratio = (size - margin) / height if is_height_greater else (size - margin) / width
        width, height = int(ratio * width), int(ratio * height)
        b3, b4 = self._centre_pad(size, width) if is_height_greater else self._centre_pad(size, height)

        if is_height_greater:
            return b1, b2, b3, b4
        else:
            return b3, b4, b1, b2

    def _centre_pad(self, size, side):
        if side % 2 == 0:
            side_1 = int((size - side) / 2)
            sid2_2 = side_1
        else:
            side_1 = int((size - side) / 2)
            sid2_2 = side_1 + 1

        return side_1, sid2_2

    def _create_grid(self):
        rows = []
        images_with_border = [cv2.copyMakeBorder(img.copy(), 1, 1, 1, 1, cv2.BORDER_CONSTANT, None,
                                                 value=constants.DIGIT_GRID_BORDER_COLOR) for img in self.digits]

        for i in range(9):
            row = np.concatenate(images_with_border[i * 9:((i + 1) * 9)], axis=1)
            rows.append(row)

        img = np.concatenate(rows)

        return img
