import operator

import cv2
import numpy as np

img = cv2.imread('data/image7.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("IMG_GRAY", img_gray)

img_processed = cv2.GaussianBlur(img_gray.copy(), (7, 7), 0)
img_processed = cv2.adaptiveThreshold(img_processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
img_processed = cv2.bitwise_not(img_processed, img_processed)

kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
img_processed = cv2.dilate(img_processed, kernel)

contours, hierarchy = cv2.findContours(img_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key=cv2.contourArea, reverse=True)
largest_contours = contours[0]

# cv2.imshow('Image', im1)
bottom_right, _ = max(enumerate([point[0][0] + point[0][1] for point in largest_contours]), key=operator.itemgetter(1))
top_left, _ = min(enumerate([point[0][0] + point[0][1] for point in largest_contours]), key=operator.itemgetter(1))
top_right, _ = max(enumerate([point[0][0] - point[0][1] for point in largest_contours]), key=operator.itemgetter(1))
bottom_left, _ = min(enumerate([point[0][0] - point[0][1] for point in largest_contours]), key=operator.itemgetter(1))

corners = [largest_contours[top_left][0], largest_contours[top_right][0], largest_contours[bottom_left][0],
           largest_contours[bottom_right][0]]

# for corner in corners:
#     print(corner)
#     cv2.drawMarker(img, (corner[0], corner[1]), (0, 0, 255), markerType=cv2.MARKER_STAR, markerSize=1, thickness=2,
#                    line_type=cv2.LINE_AA)
# break

# cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Resized_Window", 600, 600)
#
# cv2.imshow("Resized_Window", img)

top_left, top_right, bottom_left, bottom_right = corners[0], corners[1], corners[2], corners[3]

src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')


def calc_dist(p1, p2):
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]

    return np.sqrt((d1 ** 2 + d2 ** 2))


longest_side = max([
    calc_dist(top_left, top_right),
    calc_dist(top_left, bottom_left),
    calc_dist(top_right, bottom_right),
    calc_dist(bottom_left, bottom_right)
])

output_image = np.array([[0, 0], [longest_side - 1, 0], [longest_side - 1, longest_side - 1], [0, longest_side - 1]],
                        dtype='float32')

pers_transf = cv2.getPerspectiveTransform(src=src, dst=output_image)

image_crop = cv2.warpPerspective(img_gray, pers_transf, (int(longest_side), int(longest_side)))

squares = []

small_sq_sides = image_crop.shape[:1][0]/9

for i in range(9):
    for j in range(9):
        point1 = (i*small_sq_sides, j*small_sq_sides)
        point2 = ((i+1)*small_sq_sides, (j+1)*small_sq_sides)
        squares.append((point1, point2))

print(squares)
#
# print(output_image)
# print(src)
# print(longest_side)
#
# cv2.imshow("Cropped Image", image_crop)

cv2.waitKey(0)
cv2.destroyAllWindows()
