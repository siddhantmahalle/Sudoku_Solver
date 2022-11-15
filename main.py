from sudoku_extractor import image_processor, digit_extractor, utils
from digit_reconizer import digit_recognizer
from sudoku_solver import solve


if __name__ == '__main__':

    path = 'data/image220.jpg'

    img = image_processor.Process(path=path)
    extracted_image = img.extract_image()
    utils.show_image("Extracted_Image", extracted_image)

    digits = digit_extractor.Extract(img=extracted_image)
    image_grid = digits.get_image_grid()
    utils.show_image("Image_grid", image_grid)

    sudoku = digit_recognizer.Recognise(img=image_grid)
    sudoku_array = sudoku.get_sudoku_array()
    print(sudoku_array)

    solution = solve.Solve(sudoku_array)
    final_grid = solution.solve_sudoku()

    print(final_grid)
