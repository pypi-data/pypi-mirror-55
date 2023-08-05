import base64
import cv2
import numpy as np


def base64_to_img(str,rgb = True):
    """
    convert base64 string to numpy image
    :param str: (string)base64 encoded string of image
    :param rgb: (Bool)if decoded image is rgb,
    :return:
    """
    mode = 0
    if rgb:
        mode = 1
    img = base64.b64decode(str)
    img_np = np.fromstring(img, np.uint8)
    img = cv2.imdecode(img_np,mode)
    return img


def base64_from_file(path):
    """
    get base64 image string from file path
    :param path: (string)path to image file
    :return: (string)base64 image string
    """
    with open(path, 'rb') as handler:
        return base64.b64encode(handler.read()).decode('utf-8')