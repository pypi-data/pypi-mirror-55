import cv2
import matplotlib.pyplot as plt


def show_img_np(np_array, size=20, save=False):
    """
    :param np_array: input image, one channel or 3 channel,
    :param save: if save image
    :param size: image canvas size, in inches
    :return:
    """
    if len(np_array.shape) < 3:
        plt.rcParams['image.cmap'] = 'gray'
    img_np = np_array
    plt.figure(figsize=(size, size), facecolor='w', edgecolor='k')
    plt.imshow(img_np)
    if save:
        cv2.imwrite('debug.png', img_np)
    else:
        plt.show()
