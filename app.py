from flask import Flask, render_template, url_for, request
from PIL import Image, ImageOps
from keras.models import load_model
import numpy as np
import base64
import io
import re


app = Flask(__name__)

# Loading the model
Model_Path = "Models/lenet0.h5"
print("Model is loading...!")
model = load_model(Model_Path)
print("Model is loaded.Check at http://127.0.0.1:5000/")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():

    imgData = request.get_data(as_text=True)
    convertImage(imgData)
    image_file = 'output.png'

    result = predict_char(image_file, model)
    print(imgData)
    return result


# Decoding an image from base64 into raw representation

def convertImage(imgData):
    imgstr = re.search(r'base64,(.*)', imgData).group(1)
    base64_img = imgstr
    base64_img_bytes = base64_img.encode('utf-8')
    with open('output.png', 'wb') as output:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        output.write(decoded_image_data)
    return None

# Predicting the number


def rgba2rgb(rgba, background=(255, 255, 255)):
    row, col, ch = rgba.shape

    if ch == 3:
        return rgba

    assert ch == 4, 'RGBA image has 4 channels.'

    rgb = np.zeros((row, col, 3), dtype='float32')
    r, g, b, a = rgba[:, :, 0], rgba[:, :, 1], rgba[:, :, 2], rgba[:, :, 3]

    a = np.asarray(a, dtype='float32') / 255.0

    R, G, B = background

    rgb[:, :, 0] = r * a + (1.0 - a) * R
    rgb[:, :, 1] = g * a + (1.0 - a) * G
    rgb[:, :, 2] = b * a + (1.0 - a) * B

    return np.asarray(rgb, dtype='uint8')


def resize(img, size):
    img = Image.fromarray(img)
    resized_img = img.resize(size, Image.ANTIALIAS)
    resized_img_array = np.asarray(resized_img)
    return resized_img_array


def reshape(img, shape):
    img = np.reshape(img, shape)
    return img


def crop(img):
    image = Image.fromarray(img)
    imageBox = image.getbbox()
    cropped_img = image.crop(imageBox)
    cropped_img_array = np.asarray(cropped_img)
    return cropped_img_array


def invert(img):
    img = Image.fromarray(img)
    inverted_img = ImageOps.invert(img)
    inverted_img_array = np.asarray(inverted_img)
    return inverted_img_array


def min_max_scalar(img, scale_range=(0, 1)):

    px_min = scale_range[0]
    px_max = scale_range[1]
    img = img.astype('float32')
    img = img/img.max()
    scaled_img = img * (px_max - px_min) + px_min
    return scaled_img


char_dict = {0: 'অ', 1: 'আ', 2: 'ই', 3: 'ঈ', 4: 'উ', 5: 'ঊ', 6: 'ঋ', 7: 'এ', 8: 'ঐ', 9: 'ও', 10: 'ঔ',
             11: 'ক', 12: 'খ', 13: 'গ', 14: 'ঘ', 15: 'ঙ', 16: 'চ', 17: 'ছ', 18: 'জ', 19: 'ঝ', 20: 'ঞ',
             21: 'ট', 22: 'ঠ', 23: 'ড', 24: 'ঢ', 25: 'ণ', 26: 'ত', 27: 'থ', 28: 'দ', 29: 'ধ', 30: 'ন',
             31: 'প', 32: 'ফ', 33: 'ব', 34: 'ভ', 35: 'ম', 36: 'য',  37: 'র',  38: 'ল', 39: 'শ', 40: 'ষ',
             41: 'স', 42: 'হ', 43: 'ড়', 44: 'ঢ়', 45: 'য়', 46: 'ৎ', 47: ' ং', 48: ' ঃ', 49: ' ঁ '}


def predict_char(image_file, model):
    img = Image.open(image_file)
    img = np.asarray(img)
    img = rgba2rgb(img)
    img = invert(img)
    img = crop(img)
    img = invert(img)
    img = resize(img, (64, 64))
    img = reshape(img, (-1, 64, 64, 3))
    img = min_max_scalar(img)
    result = model.predict(img).argmax()
    result_char = char_dict[result]
    return result_char


if __name__ == '__main__':

    app.run(debug=True)
