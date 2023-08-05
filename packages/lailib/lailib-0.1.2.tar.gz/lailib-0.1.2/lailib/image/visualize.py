import matplotlib.pyplot as plt
import cv2


def show_img_np(np_array, size=20, save=False, cmap='gray'):
    """
    :param np_array: input image, one channel or 3 channel,
    :param save: if save image
    :param size: image canvas size, in inches
    :return:
    """
    if len(np_array.shape) < 3:
        plt.rcParams['image.cmap'] = cmap
    img_np = np_array
    plt.figure(figsize=(size, size), facecolor='w', edgecolor='k')
    plt.imshow(img_np)
    if save:
        cv2.imwrite('debug.png', img_np)
    else:
        plt.show()
