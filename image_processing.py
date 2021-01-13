import cv2 as cv
import os

from other_functions import generate_imagename

class ImageEditor:

    def __init__(self):
        pass

    def convert_to_hsv(self, path):
        image = cv.imread(path)
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), hsv)

        return edited_image_name

    def convert_to_gray(self, path):
        image = cv.imread(path)
        hsv = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), hsv)

        return edited_image_name

    def convert_to_lab(self, path):
        image = cv.imread(path)
        hsv = cv.cvtColor(image, cv.COLOR_BGR2LAB)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), hsv)

        return edited_image_name

    def convert_to_rgb(self, path):
        image = cv.imread(path)
        hsv = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), hsv)

        return edited_image_name




