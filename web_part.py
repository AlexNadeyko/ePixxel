import os
import random
import string
import image_processing
import numpy as np

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from image_processing import ImageEditor, GradientType
from other_functions import generate_imagename

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'

image_editor = ImageEditor()


@app.route('/')
def index():
    return render_template('start_page.html')


@app.route('/start_page')
def start_page():
    return render_template('start_page.html')


@app.route('/main_page/<image_name>')
def main_page(image_name):
    return render_template('main_page.html', filename=image_name)


@app.route('/main_page/<image_name>', methods=['POST'])
def upload_image(image_name):
    uploaded_image = request.files['file']

    if uploaded_image.filename != '':
        file_extension = uploaded_image.filename.split('.')[1]
        new_image_name = generate_imagename(file_extension)
        uploaded_image.save(os.path.join(app.config['UPLOAD_PATH'], new_image_name))

    return redirect(url_for('main_page', image_name=new_image_name))


@app.route('/upload/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_PATH'], filename), as_attachment=True, attachment_filename=filename)


@app.route('/main_page/<filename>/<mode>', methods=["POST"])
def operation(filename, mode):

    if mode == 'color_space':
        if request.form['colorButton'] == 'convertToHSV':
            path_new_image = image_editor.convert_to_hsv(os.path.join(app.config['UPLOAD_PATH'], filename))

        elif request.form['colorButton'] == 'convertToGRAY':
            path_new_image = image_editor.convert_to_gray(os.path.join(app.config['UPLOAD_PATH'], filename))

        elif request.form['colorButton'] == 'convertToLAB':
            path_new_image = image_editor.convert_to_lab(os.path.join(app.config['UPLOAD_PATH'], filename))

        elif request.form['colorButton'] == 'convertToRGB':
            path_new_image = image_editor.convert_to_rgb(os.path.join(app.config['UPLOAD_PATH'], filename))

    elif mode == 'geometric_transformation':

        if request.form['transformationButton'] == 'scale':

            if request.form['radioUnits'] == 'px':
                width = int(request.form['textInputWidthSize'])
                height = int(request.form['textInputHeightSize'])

                path_new_image = image_editor.scale_pixels(os.path.join(app.config['UPLOAD_PATH'], filename), width,
                                                           height)

            elif request.form['radioUnits'] == 'perc':
                width = int(request.form['textInputWidthSize'])
                height = int(request.form['textInputHeightSize'])

                path_new_image = image_editor.scale_percents(os.path.join(app.config['UPLOAD_PATH'], filename), width,
                                                           height)

        elif request.form['transformationButton'] == 'rotate':
            angle = int(request.form['textInputAngle'])
            path_new_image = image_editor.rotate(os.path.join(app.config['UPLOAD_PATH'], filename), angle)

        elif request.form['transformationButton'] == 'crop':
            crop_top = int(request.form['textInputTopCrop'])
            crop_bottom = int(request.form['textInputBottomCrop'])
            crop_left = int(request.form['textInputLeftCrop'])
            crop_right = int(request.form['textInputRightCrop'])

            path_new_image = image_editor.crop(os.path.join(app.config['UPLOAD_PATH'], filename), crop_top,
                                                 crop_bottom, crop_left, crop_right)

    elif mode == 'smooth':

        if request.form['blurButton'] == 'gaussian_blur':
            height_kernel = int(request.form['textInputKernelHeight'])
            width_kernel = int(request.form['textInputKernelWidth'])

            path_new_image = image_editor.gaussian_blur(os.path.join(app.config['UPLOAD_PATH'], filename), width_kernel,
                                                        height_kernel)

        elif request.form['blurButton'] == 'median_blur':
            kernel_median_value = int(request.form['textInputKernelMedianValue'])

            path_new_image = image_editor.median_blur(os.path.join(app.config['UPLOAD_PATH'], filename),
                                                      kernel_median_value)

    elif mode == 'edge_detecting':

        if request.form['edgeDetectionButton'] == 'edge_detecting_manual':
            min_value = int(request.form['textInputMinValueEdge'])
            max_value = int(request.form['textInputMaxValueEdge'])

            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), min_value,
                                                       max_value)

        elif request.form['edgeDetectionButton'] == 'template_1':
            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), 50, 50)

        elif request.form['edgeDetectionButton'] == 'template_2':
            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), 50, 100)

        elif request.form['edgeDetectionButton'] == 'template_3':
            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), 50, 150)

        elif request.form['edgeDetectionButton'] == 'template_4':
            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), 50, 200)

        elif request.form['edgeDetectionButton'] == 'template_5':
            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), 50, 300)

        elif request.form['edgeDetectionButton'] == 'template_6':
            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), 100, 300)

        elif request.form['edgeDetectionButton'] == 'template_7':
            path_new_image = image_editor.detect_edges(os.path.join(app.config['UPLOAD_PATH'], filename), 100, 150)

    elif mode == 'gradient':

        if request.form['gradientButton'] == 'x_direction':
            path_new_image = image_editor.gradient(os.path.join(app.config['UPLOAD_PATH'], filename),
                                                   GradientType.X_Direction)

        elif request.form['gradientButton'] == 'y_direction':
            path_new_image = image_editor.gradient(os.path.join(app.config['UPLOAD_PATH'], filename),
                                                   GradientType.Y_Direction)

        elif request.form['gradientButton'] == 'x_y_direction':
            path_new_image = image_editor.gradient(os.path.join(app.config['UPLOAD_PATH'], filename),
                                                   GradientType.X_Y_Direction)

    elif mode == 'filter':

        if request.form['filterButton'] == 'cartoon_filter':
            path_new_image = image_editor.cartoon_filter(os.path.join(app.config['UPLOAD_PATH'], filename))

        elif request.form['filterButton'] == 'watercolor_filter':
            path_new_image = image_editor.watercolor_filter(os.path.join(app.config['UPLOAD_PATH'], filename))

        elif request.form['filterButton'] == 'sketch_filter':
            path_new_image = image_editor.sketch_filter(os.path.join(app.config['UPLOAD_PATH'], filename))

        elif request.form['filterButton'] == 'black_white_sketch_filter':
            path_new_image = image_editor.black_white_sketch_filter(os.path.join(app.config['UPLOAD_PATH'], filename))

        elif request.form['filterButton'] == 'colored_sketch_filter':
            path_new_image = image_editor.colored_sketch_filter(os.path.join(app.config['UPLOAD_PATH'], filename))

    return redirect(url_for('main_page', image_name=path_new_image))


if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_PATH']):
        os.makedirs(app.config['UPLOAD_PATH'])

    app.run()


