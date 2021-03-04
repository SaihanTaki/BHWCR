from PIL import Image, ImageOps
import numpy as np


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


def invert(img):
    img = Image.fromarray(img)
    inverted_img = ImageOps.invert(img)
    inverted_img_array = np.asarray(inverted_img)
    return inverted_img_array


def crop(img):
    image = Image.fromarray(img)
    imageBox = image.getbbox()
    cropped_img = image.crop(imageBox)
    cropped_img_array = np.asarray(cropped_img)
    return cropped_img_array


def min_max_scalar(img, scale_range=(0, 1)):

    px_min = scale_range[0]
    px_max = scale_range[1]
    img = img.astype('float32')
    img = img/img.max()
    scaled_img = img * (px_max - px_min) + px_min
    return scaled_img


def improve_image_quality(img, n=5):

    for _ in range(n):
        mask = np.logical_and(img > 0.0, img < 0.2)
        img[mask] = 0.0
        img = img + 0.1
        img[img > 1.0] = 1.0
        img[img == 0.1] = 0.0

    return img


char_dict = {0: 'অ', 1: 'আ', 2: 'ই', 3: 'ঈ', 4: 'উ', 5: 'ঊ', 6: 'ঋ', 7: 'এ', 8: 'ঐ', 9: 'ও', 10: 'ঔ',
             11: 'ক', 12: 'খ', 13: 'গ', 14: 'ঘ', 15: 'ঙ', 16: 'চ', 17: 'ছ', 18: 'জ', 19: 'ঝ', 20: 'ঞ',
             21: 'ট', 22: 'ঠ', 23: 'ড', 24: 'ঢ', 25: 'ণ', 26: 'ত', 27: 'থ', 28: 'দ', 29: 'ধ', 30: 'ন',
             31: 'প', 32: 'ফ', 33: 'ব', 34: 'ভ', 35: 'ম', 36: 'য',  37: 'র',  38: 'ল', 39: 'শ', 40: 'ষ',
             41: 'স', 42: 'হ', 43: 'ড়', 44: 'ঢ়', 45: 'য়', 46: 'ৎ', 47: ' ং', 48: ' ঃ', 49: ' ঁ ', 50: '০',
             51: '১', 52: '২', 53: '৩', 54: '৪', 55: '৫', 56: '৬', 57: '৭', 58: '৮', 59: '৯'}
