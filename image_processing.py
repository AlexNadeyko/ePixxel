import cv2 as cv
import os
import enum

from other_functions import generate_imagename

class GradientType(enum.Enum):
   X_Direction = 1
   Y_Direction = 2
   X_Y_Direction = 3


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
        rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), rgb)

        return edited_image_name

    def scale_percents(self, path, scale_percent_x=50, scale_percent_y=50):
        image = cv.imread(path)

        width = int(image.shape[1] * scale_percent_x / 100)
        height = int(image.shape[0] * scale_percent_y / 100)

        dsize = (width, height)

        res = cv.resize(image, dsize)

        file_extension = path.split('.')[1]
        edited_image_name =  generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def scale_pixels(self, path, scale_pixels_x=50, scale_pixels_y=50):
        image = cv.imread(path)

        width = scale_pixels_x
        height = scale_pixels_y

        dsize = (width, height)

        res = cv.resize(image, dsize)

        file_extension = path.split('.')[1]
        edited_image_name =  generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def rotate(self, path, rotate_angle=90):
        image = cv.imread(path)

        angle = rotate_angle
        height, width = image.shape[0:2]

        rotation_matrix = cv.getRotationMatrix2D((width / 2, height / 2), angle, .5)
        # rotation_matrix = cv.getRotationMatrix2D((width/2, height/2), angle, 1)
        res = cv.warpAffine(image, rotation_matrix, (width, height))

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def crop(self, path, crop_top=10, crop_bottom=10, crop_left=10, crop_right=10):
        image = cv.imread(path)

        height, width = image.shape[0:2]
        print(.15)

        start_row = int(height * crop_top/100)

        start_col = int(width * crop_left/100)

        end_row = int(height * ((100-crop_bottom)/100))

        end_col = int(width * ((100 - crop_right)/100))

        res = image[start_row:end_row, start_col:end_col]

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def gaussian_blur(self, path, width_kernel, height_kernel):
        image = cv.imread(path)

        res = cv.GaussianBlur(image, (width_kernel, height_kernel), 0)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def median_blur(self, path, kernel_median_value):
        image = cv.imread(path)

        res = cv.medianBlur(image, kernel_median_value)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def detect_edges(self, path, min_value, max_value):
        image = cv.imread(path)

        res = cv.Canny(image, min_value, max_value)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def gradient(self, path, gradient_type):
        image = cv.imread(path)

        if gradient_type == GradientType.X_Direction:
            res = cv.Sobel(image, cv.CV_8UC1, 1, 0)
        elif gradient_type == GradientType.Y_Direction:
            res = cv.Sobel(image, cv.CV_8UC1, 0, 1)
        elif gradient_type == GradientType.X_Y_Direction:
            image_x = cv.Sobel(image, cv.CV_8UC1, 0, 1)
            image_y = cv.Sobel(image, cv.CV_8UC1, 1, 0)
            res = cv.add(image_x, image_y)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def sketch_filter(self, path):
        image = cv.imread(path)
        img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        img_blur = cv.GaussianBlur(img_gray, (21, 21), 0, 0)
        img_blend = cv.divide(img_gray, img_blur, scale=256)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), img_blend)

        return edited_image_name

    def sketch_filter_canvas(self, path):
        image = cv.imread(path)
        img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        canvas = cv.imread(path, cv.CV_8UC1)

        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        img_blur = cv.GaussianBlur(img_gray, (21, 21), 0, 0)
        img_blend = cv.divide(img_gray, img_blur, scale=256)

        img_blend = cv.multiply(img_blend, canvas, scale=1. / 256)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), img_blend)

        return edited_image_name

    def watercolor_filter(self, path):
        image = cv.imread(path)
        res = cv.stylization(image, sigma_s=60, sigma_r=0.6)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def black_white_sketch_filter(self, path):
        image = cv.imread(path)

        res, _ = cv.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def colored_sketch_filter(self, path):
        image = cv.imread(path)

        _, res = cv.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name

    def cartoon_filter(self, path):
        image = cv.imread(path)

        res = cv.stylization(image, sigma_s=150, sigma_r=0.25)

        file_extension = path.split('.')[1]
        edited_image_name = generate_imagename(file_extension)

        cv.imwrite(os.path.join('uploads', edited_image_name), res)

        return edited_image_name


