import cv2


def otsu_thresh(im):
    '''
    binarize image with otsu algorithm
    :param im(ndarray): uint8 numpy array
    :return: binarized image as uint8 numpy array
    '''
    _, binarized = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binarized


def vanilla_thresh(im, th=128):
    '''
    binarize image with given threshold(default is 128)
    :param im(ndarray): uint8 numpy array
    :param th(int): threshold
    :return: binarized image as uint8 numpy array
    '''
    _, binarized = cv2.threshold(im, 0, th, cv2.THRESH_BINARY)
    return binarized
