from sudoku_extractor import image_extractor, digit_recognizer
from sudoku_solver import solve

if __name__ == '__main__':

    path = 'data/image8.jpg'

    img = image_extractor.Extract(path=path)
    extracted_image = img.extract_image()

