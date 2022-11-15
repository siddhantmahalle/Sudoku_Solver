import numpy as np
import cv2

from config import constants


def show_image(name: str, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_distance(p1, p2):
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]

    return np.sqrt((d1 ** 2 + d2 ** 2))


def get_preprocessed_image(img, get_dilated_img: bool):
    dilate_kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)

    img_processed = cv2.GaussianBlur(img.copy(),
                                     (constants.GAUSSIAN_BLUR_KSIZE, constants.GAUSSIAN_BLUR_KSIZE), 0)
    img_processed = cv2.adaptiveThreshold(img_processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C | cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 5, 2)
    img_processed = cv2.bitwise_not(img_processed, img_processed)

    if get_dilated_img:
        img_processed = cv2.dilate(img_processed, dilate_kernel)

    return img_processed



