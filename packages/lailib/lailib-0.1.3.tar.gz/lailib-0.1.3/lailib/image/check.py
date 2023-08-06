import numpy as np


def check_img_format(img, check_color_space=True, isrgb=False):
    """
    check image format, must be uint8 numpy array
    :param img: (numpy array)input image
    :param check_color_space: (bool) do checking on color space, if False, both gray and rgb image are supported
    :param isrgb: (boolean)check if image is colored, True for must colored, False for must be gray.
    :return: None
    """
    s = img.shape
    if check_color_space:
        if isrgb and len(s) != 3:
            raise ValueError("Image should be colored, got gray")
        if (not isrgb) and len(s) != 2:
            raise ValueError("Image should be gray, got 3D array with shape of {}".format(str(s)))
    try:
        if img.dtype != np.array([1], dtype=np.uint8).dtype:
            raise ValueError("Image should be numpy array with data type of uint8")
    except Exception:
        raise ValueError("Image should be numpy array with data type of uint8")
