import cv2
import numpy as np

from lailib.image.check import check_img_format


def jpg_compress(img, quality=30):
    """
    add jpg compress noise to image
    :param img: (numpy uint8)input image
    :param quality: (int)0-100, jpeg compress quality, lower is lower quality
    :return: (numpy uint8)compressed image
    """
    check_img_format(img, check_color_space=False)
    grey = len(img.shape) == 2
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, result = cv2.imencode('.jpg', np.uint8(img), encode_param)
    if grey:
        result = cv2.imdecode(result, 0)
    else:
        result = cv2.imdecode(result, 1)
    return result
