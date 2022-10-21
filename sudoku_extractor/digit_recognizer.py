import operator

import cv2
import numpy as np

from sudoku_extractor.utils import *
from config import constants


class Recognise:
    def __init__(self, img):
        self.img = img
        self.length_digits = img.shape[:1][0] / 9
        self.squares = self._get_digit_corners()


    def _get_digit_corners(self):
        squares = []
        for i in range(9):
            for j in range(9):
                point1 = (i * self.length_digits, j * self.length_digits)
                point2 = ((i + 1) * self.length_digits, (j + 1) * self.length_digits)
                squares.append((point1, point2))

        return squares

    def _extract_digits(self):
