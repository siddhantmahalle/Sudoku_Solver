import operator

import cv2
import numpy as np

from sudoku_extractor.utils import *
from config import constants


class Process:

    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

        self.img_processed = None
        self.contours = None
        self.largest_contours = None
        self.corners = None
        self.cropped_image = None

    def extract_image(self):

        self.img_processed = get_preprocessed_image(self.img, get_dilated_img=True)

        self.contours = self._get_contours()
        self.contours = sorted(self.contours, key=cv2.contourArea, reverse=True)
        self.largest_contours = self.contours[0]

        self.corners = self._get_corners()
        self.cropped_image = self._get_cropped_image()

        return self.cropped_image

    def _get_contours(self):
        contours, hierarchy = cv2.findContours(self.img_processed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def _get_corners(self):
        bottom_right, _ = max(enumerate([point[0][0] + point[0][1] for point in self.largest_contours]),
                              key=operator.itemgetter(1))
        top_left, _ = min(enumerate([point[0][0] + point[0][1] for point in self.largest_contours]),
                          key=operator.itemgetter(1))
        top_right, _ = max(enumerate([point[0][0] - point[0][1] for point in self.largest_contours]),
                           key=operator.itemgetter(1))
        bottom_left, _ = min(enumerate([point[0][0] - point[0][1] for point in self.largest_contours]),
                             key=operator.itemgetter(1))

        corners = [self.largest_contours[top_left][0], self.largest_contours[top_right][0],
                   self.largest_contours[bottom_left][0], self.largest_contours[bottom_right][0]]

        return corners

    def _get_cropped_image(self):
        top_left, top_right, bottom_left, bottom_right = self.corners[0], self.corners[1], self.corners[2], self.corners[3]

        src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')

        longest_side = max([
            get_distance(top_left, top_right),
            get_distance(top_left, bottom_left),
            get_distance(top_right, bottom_right),
            get_distance(bottom_left, bottom_right)
        ])

        output_image = np.array([[0, 0], [longest_side - 1, 0], [longest_side - 1, longest_side - 1],
                                 [0, longest_side - 1]], dtype='float32')
        perspective_transform = cv2.getPerspectiveTransform(src=src, dst=output_image)
        cropped_image = cv2.warpPerspective(self.img, perspective_transform, (int(longest_side), int(longest_side)))

        return cropped_image

    # def
    #
    # def _extract_image(self, img):
