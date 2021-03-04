from flask import Flask, render_template, url_for, request
from PIL import Image, ImageOps
from keras.models import load_model
from utils import *
import numpy as np
import base64
import io
import re


app = Flask(__name__)

# Loading the model
Model_Path = "Models/FineTunedMobileNet.h5"
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


def predict_char(image_file, model):
    img = Image.open(image_file)
    img = np.asarray(img)
    img = rgba2rgb(img)
    img = invert(img)
    img = crop(img)
    img = resize(img, (64, 64))
    img = reshape(img, (-1, 64, 64, 3))
    img = min_max_scalar(img)
    img = improve_image_quality(img)
    result = model.predict(img).argmax()
    result_char = char_dict[result]
    return result_char


if __name__ == '__main__':

    app.run(debug=True)
