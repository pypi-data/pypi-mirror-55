import base64
from collections import namedtuple
import cv2
import numpy as np


def base64_to_img(str, rgb=True):
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
    img_np = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img_np, mode)
    return img


def base64_from_file(path):
    """
    get base64 image string from file path
    :param path: (string)path to image file
    :return: (string)base64 image string
    """
    with open(path, 'rb') as handler:
        return base64.b64encode(handler.read()).decode('utf-8')


def split_square_img_boarder(img, h=256, w=256, boarder=25):
    """
    split image into a bag of small images for batch training
    :param img: input image
    :param h: height of bag of small image
    :param w: width of bag of small image
    :param boarder: to eliminate artifact, how far boarder of small image to discard
    :return: list of namedtuple of (y:y_coord of lr corner of the small image,
                                    x:x_coord of lr corner of the small image,
                                    img:small image)
    """
    b=boarder*2
    img_h, img_w = img.shape[0], img.shape[1]
    if img_h < h or img_w < w:
        raise ValueError("input image should be larger than split img")
    if h<b:
        raise ValueError("boarder is too large")
    h_start = 0
    w_start = 0
    h_start_list = []
    w_start_list = []
    while h_start + h < img_h:
        h_start_list.append(h_start)
        h_start += (h - b)
    while w_start + h < img_w:
        w_start_list.append(w_start)
        w_start += (w - b)
    h_start_list.append(img_h - h)
    w_start_list.append(img_w - w)
    #     print(h_start_list)
    #     print(w_start_list)
    meta = namedtuple('meta',['y','x','img'])
    split_list = []
    for i in h_start_list:
        for j in w_start_list:
            if len(img.shape) == 3:
                split_list.append(meta(i, j, img[i:i + h, j:j + w, :]))
            else:
                split_list.append(meta(i, j, img[i:i + h, j:j + w]))
    return split_list


def combine_square_img_boarder(metas, boarder=25):
    """
    combine bag of small image back into original one
    :param metas: bag of small image,
                  list of namedtuple of (y:y_coord of lr corner of the small image,
                                         x:x_coord of lr corner of the small image,
                                         img:small image)
    :param boarder: to eliminate artifact, how far boarder of small image to discard,
    should be the same as split function
    :return: original image
    """
    square_h = metas[0].img.shape[0]
    square_w = metas[0].img.shape[1]
    img_h = max(x.y for x in metas) + square_h
    img_w = max(x.x for x in metas) + square_w

    #     print(img_h,img_w)
    if len(metas[0].img.shape) == 3:
        blank_img = np.zeros((img_h, img_w,3))

        for i in metas:
            blank_img[i.y:i.y + square_h, i.x:i.x + square_w,:] = i.img
        for i in metas:
            w_boarder, s_boarder, a_boarder, d_boarder = boarder, boarder, boarder, boarder
            blank_img[i.y + boarder:i.y + square_h - boarder,
            i.x + boarder:i.x + square_w - boarder,:] = i.img[boarder:-boarder, boarder:-boarder,:]


    else:
        blank_img = np.zeros((img_h, img_w))
        for i in metas:
            blank_img[i.y:i.y + square_h, i.x:i.x + square_w] = i.img
        for i in metas:
            w_boarder, s_boarder, a_boarder, d_boarder = boarder, boarder, boarder, boarder
            blank_img[i.y + boarder:i.y + square_h - boarder,
                      i.x + boarder:i.x + square_w - boarder] = i.img[boarder:-boarder,boarder:-boarder]
    return blank_img