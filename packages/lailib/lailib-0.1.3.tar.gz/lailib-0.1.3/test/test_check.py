import pytest

from lailib.image.check import *


class TestCheckImgFormat:
    def test_acc_color(self):
        img = np.array(np.random.rand(128, 256, 3) * 255, dtype=np.uint8)
        check_img_format(img, isrgb=True)
        with pytest.raises(ValueError):
            check_img_format(img, isrgb=False)

    def test_acc_gray(self):
        img = np.array(np.random.rand(128, 256) * 255, dtype=np.uint8)
        check_img_format(img)
        with pytest.raises(ValueError):
            check_img_format(img, isrgb=True)

    def test_acc_multichannel(self):
        img = np.array(np.random.rand(4000, 4000, 4) * 255, dtype=np.uint8)
        with pytest.raises(ValueError):
            check_img_format(img, isrgb=False)

    def test_acc_one_channel(self):
        img = np.array(np.random.rand(256) * 255, dtype=np.uint8)
        with pytest.raises(ValueError):
            check_img_format(img, isrgb=True)
        with pytest.raises(ValueError):
            check_img_format(img, isrgb=False)
