import cv2
import numpy
import numpy as np

from tensorflow.keras import models
from sudoku_extractor.utils import show_image
import json


class Recognise:

    def __init__(self, img):
        self.img = img
        self.model_path = 'models/CNN/model.json'
        self.weights_path = 'models/CNN/model.h5'
        self.model = self._load_model()
        self.model.load_weights(self.weights_path)

    def _load_model(self):

        with open(self.model_path, "r") as file:
            json_string = file.read()

        model = models.model_from_json(json_string=json_string)
        return model

    def get_sudoku_array(self):
        # sudoku_img = cv2.resize(self.img, (450, 450))
        sudoku_img = self.img
        grid = np.zeros([9, 9])

        for i in range(9):
            for j in range(9):
                image = sudoku_img[i * 37:(i + 1) * 37, j * 37:(j + 1) * 37]
                image = image[3:34, 3:34]

                image_sum = image.sum()

                if image_sum > 10000:
                    grid[i][j] = self._recognize_digit(image)
                else:
                    grid[i][j] = 0

        grid = grid.astype(int)

        return grid

    def _recognize_digit(self, img):
        img1 = cv2.resize(img, (28, 28))
        img2 = img1.reshape(1, 28, 28, 1)

        pred = self.model.predict(img2, verbose=0)
        pred = np.argmax(pred, axis=-1)
        return pred[0]
