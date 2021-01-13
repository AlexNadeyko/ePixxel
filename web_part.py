import os
import random
import string
import image_processing
import numpy as np

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from image_processing import ImageEditor

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

    if request.form['colorButton'] == 'convertToHSV':
        path_new_image = image_editor.convert_to_hsv(os.path.join(app.config['UPLOAD_PATH'], filename))
    elif request.form['colorButton'] == 'convertToGRAY':
        path_new_image = image_editor.convert_to_gray(os.path.join(app.config['UPLOAD_PATH'], filename))
    elif request.form['colorButton'] == 'convertToLAB':
        path_new_image = image_editor.convert_to_lab(os.path.join(app.config['UPLOAD_PATH'], filename))
    elif request.form['colorButton'] == 'convertToRGB':
        path_new_image = image_editor.convert_to_rgb(os.path.join(app.config['UPLOAD_PATH'], filename))

    return redirect(url_for('main_page', image_name=path_new_image))


def generate_imagename(extension):
    number_of_characters = 7
    image_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_characters))
    image_name = image_name + '.' + extension
    print(image_name)

    return image_name


if __name__ == "__main__":
    app.run()


