import pytest

from lailib.image.augment import *


class TestJPGCompress:
    def test_acc_mc(self):
        img_rgb = np.array(np.random.rand(802, 604, 3) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb)
        assert img_re.shape == img_rgb.shape

    def test_acc_m(self):
        img_rgb = np.array(np.random.rand(128, 256) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb)
        assert img_re.shape == img_rgb.shape

    def test_acc_xlc(self):
        img_rgb = np.array(np.random.rand(4000, 4000, 3) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb)
        assert img_re.shape == img_rgb.shape

    def test_acc_xsc(self):
        img_rgb = np.array(np.random.rand(2, 2, 3) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb)
        assert img_re.shape == img_rgb.shape

    def test_acc_xl(self):
        img_rgb = np.array(np.random.rand(4000, 4000) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb)
        assert img_re.shape == img_rgb.shape

    def test_acc_xs(self):
        img_rgb = np.array(np.random.rand(2, 2) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb)
        assert img_re.shape == img_rgb.shape

    def test_acc_low_qual(self):
        img_rgb = np.array(np.random.rand(800, 458, 3) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb, 0)
        assert img_re.shape == img_rgb.shape

    def test_acc_high_qual(self):
        img_rgb = np.array(np.random.rand(128, 256, 3) * 255, dtype=np.uint8)
        img_re = jpg_compress(img_rgb, 100)
        assert img_re.shape == img_rgb.shape

    def test_float_c(self):
        img_rgb = np.random.rand(128, 256, 3)
        with pytest.raises(ValueError):
            img_re = jpg_compress(img_rgb)

    def test_float(self):
        img_rgb = np.random.rand(128, 256)
        with pytest.raises(ValueError):
            img_re = jpg_compress(img_rgb)
