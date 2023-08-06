import numpy as np
import cv2
from lailib.image.binarize import otsu_thresh
import random


def random_sample(imgs, target_h=256, target_w=256, size_aug_min=0.25, size_aug_max=4, skew_aug=2,
                  randomizer='uniform_exp'):
    """
    random sample parts from images with the same size
    :param img: original image
    :param target_h: output h
    :param target_w: output w
    :param size_aug_min: min zoom scale when sampling image (sample bigger parts and zoom out)
    :param size_aug_max: max zoom scale when sampling image (sample smaller parts and zoom in)
    :param skew_aug: scale for random stretching image when sampling (augmentation)
    :param randomizer: randomize method when randomizing sample scale
    :return: sampled image
    """
    size_aug_min,size_aug_max = 1/size_aug_max,1/size_aug_min
    img = imgs[0]
    if len(img.shape) == 3:
        if_color = True
        h, w, _ = img.shape
    else:
        h, w = img.shape
        if_color = False
    if randomizer == 'uniform':
        size_aug = random.uniform(1 / size_aug_min, 1 / size_aug_max)
    elif randomizer == 'uniform_exp':
        size_aug = np.exp(random.uniform(np.log(1 / size_aug_min), np.log(1 / size_aug_max)))
    else:
        raise ValueError('randomizer not supported')
    if size_aug_min*min(h,w)<1:
        raise ValueError('lower size limit is too small')

    skew_aug = np.exp(random.uniform(-np.log(skew_aug), np.log(skew_aug)))
    size_aug = np.min([size_aug, h / target_h / np.sqrt(skew_aug), w / target_w * np.sqrt(skew_aug)])
    crop_h, crop_w = int(target_h * size_aug * np.sqrt(skew_aug)), int(target_w * size_aug / np.sqrt(skew_aug))
    crop_h,crop_w = max(crop_h,1),max(crop_w,1)
    #     print(crop_h,crop_w)
    min_y, max_y, min_x, max_x = 0, h - crop_h, 0, w - crop_w

    y_start = random.randint(min_y, max_y + 1)
    x_start = random.randint(min_x, max_x + 1)
    return_imgs = []
    for img in imgs:
        if if_color:
            raw_crop = img[y_start:y_start + crop_h, x_start:x_start + crop_w, :]
        else:
            raw_crop = img[y_start:y_start + crop_h, x_start:x_start + crop_w]
        if target_h < crop_h:
            return_imgs.append(cv2.resize(raw_crop, (target_h, target_w), interpolation=cv2.INTER_CUBIC))
        else:
            return_imgs.append(cv2.resize(raw_crop, (target_h, target_w), interpolation=cv2.INTER_AREA))
    return return_imgs



def crop_boundary_and_padding(im, padding=0, binarized=None):
    '''
    crop and padding objects and text imgs with pure black border, then padding.
    ex:
    for input
        0   255 0   0
        0   255 255 0
        0   255 0   0
        0   0   0   0
    output is
        255 0
        255 255
        255 0
    :param image_cv(ndarray): input image, uint8 numpy array, assumed to be gray scale
    :param padding(int or list of ints): if padding is a scalar, padding will be applied to left, right, upside and
    downside of an image.
                    if padding is a list of size 4, each entry in the list corresponds to left, right, upside and
                    downside of an image.
    :return: cropped image (uint8)
    '''
    if len(im.shape) != 2 or im.dtype != np.uint8:
        raise TypeError('input image must be gray scale image as uint8 ndarray')
    if not binarized is None:
        if binarized.shape != im.shape:
            raise ValueError('binarized image shape {} must meet in image shape {}'.format(binarized.shape, im.shape))
        if binarized.dtype != np.uint8:
            raise TypeError('binarized mask must be uint8 ndarray')
    else:
        binarized = otsu_thresh(im)
    if np.sum(binarized) == 0:
        raise ValueError('In image for crop function is all zero')

    if isinstance(padding, int):
        padding = [padding] * 4
    elif not (isinstance(padding, list) and len(padding) == 4):
        raise TypeError('padding in crop function must be int or list of size 4')

    # use binarized image to get vertical and horizontal boundaries
    col_sums = np.sum(binarized, axis=1)
    row_start = np.where(col_sums)[0][0]
    rev_col_sum = np.flip(col_sums, axis=0)
    rev_end = np.where(rev_col_sum)[0][0]
    row_end = col_sums.shape[0] - rev_end

    row_sums = np.sum(binarized, axis=0)
    col_start = np.where(row_sums)[0][0]
    rev_row_sum = np.flip(row_sums, axis=0)
    rev_end = np.where(rev_row_sum)[0][0]
    col_end = row_sums.shape[0] - rev_end

    cropped = im[row_start:row_end, col_start:col_end]

    cropped_height, cropped_width = cropped.shape
    # TODO add rand noise to height
    final_out = np.zeros((cropped_height + padding[2] + padding[3],
                          cropped_width + padding[0] + padding[1]), dtype=np.uint8)

    out_height, out_width = final_out.shape
    # do not directly use -padding as the value for end side because it can't deal with padding = 0
    final_out[padding[2]: out_height - padding[3], padding[0]: out_width - padding[1]] = cropped
    return final_out


