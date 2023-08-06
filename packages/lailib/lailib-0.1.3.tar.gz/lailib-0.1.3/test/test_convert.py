import os
import pytest
import cv2
import numpy as np

from lailib.image.convert import *


class TestBase64:
    def test_acc_base64_color(self, tmpdir):
        img_rgb = np.array(np.random.rand(128, 256, 3) * 255, dtype=np.uint8)
        img_path = os.path.join(tmpdir, "test_color.png")
        cv2.imwrite(img_path, img_rgb)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str)
        assert img_from_str.shape == img_rgb.shape
        assert np.array_equal(img_from_str, img_rgb)

    def test_acc_base64_gray(self, tmpdir):
        img = np.array(np.random.rand(128, 256) * 255, dtype=np.uint8)
        img_path = os.path.join(tmpdir, "test_color.png")
        cv2.imwrite(img_path, img)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str, rgb=False)
        assert img_from_str.shape == img.shape
        assert np.array_equal(img_from_str, img)

    def test_acc_base64_color_xl(self, tmpdir):
        img_rgb = np.array(np.random.rand(4000, 4000, 3) * 255, dtype=np.uint8)
        img_path = os.path.join(tmpdir, "test_color.png")
        cv2.imwrite(img_path, img_rgb)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str)
        assert img_from_str.shape == img_rgb.shape
        assert np.array_equal(img_from_str, img_rgb)

    def test_acc_base64_gray_xl(self, tmpdir):
        img = np.array(np.random.rand(4000, 4000) * 255, dtype=np.uint8)
        img_path = os.path.join(tmpdir, "test_color.png")
        cv2.imwrite(img_path, img)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str, rgb=False)
        assert img_from_str.shape == img.shape
        assert np.array_equal(img_from_str, img)

    def test_acc_base64_color_xs(self, tmpdir):
        img_rgb = np.array(np.random.rand(2, 2, 3) * 255, dtype=np.uint8)
        img_path = os.path.join(tmpdir, "test_color.png")
        cv2.imwrite(img_path, img_rgb)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str)
        assert img_from_str.shape == img_rgb.shape
        assert np.array_equal(img_from_str, img_rgb)

    def test_acc_base64_gray_xs(self, tmpdir):
        img = np.array(np.random.rand(2, 2) * 255, dtype=np.uint8)
        img_path = os.path.join(tmpdir, "test_color.png")
        cv2.imwrite(img_path, img)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str, rgb=False)
        assert img_from_str.shape == img.shape
        assert np.array_equal(img_from_str, img)


class TestSplit:
    def test_acc_mc(self):
        img = np.array(np.random.rand(1280, 2560, 3) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)
        assert np.array_equal(img, re_img)

    def test_acc_mc2(self):
        img = np.array(np.random.rand(1280, 2560) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)

        assert np.array_equal(img, re_img)

    def test_acc_mc3(self):
        img = np.array(np.random.rand(300, 300, 3) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)

        assert np.array_equal(img, re_img)

    def test_acc_mc4(self):
        img = np.array(np.random.rand(512, 512) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)

        assert np.array_equal(img, re_img)

    def test_s1(self):
        img = np.array(np.random.rand(256, 256, 3) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)

        assert np.array_equal(img, re_img)

    def test_s3(self):
        img = np.array(np.random.rand(256, 256) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)

        assert np.array_equal(img, re_img)

    def test_s2(self):
        img = np.array(np.random.rand(135, 142, 3) * 255, dtype=np.uint8)
        with pytest.raises(ValueError):
            metas = split_square_img_boarder(img)

    def test_s4(self):
        img = np.array(np.random.rand(13, 12) * 255, dtype=np.uint8)
        with pytest.raises(ValueError):
            metas = split_square_img_boarder(img)

    def test_s5(self):
        img = np.array(np.random.rand(257, 257) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)
        assert np.array_equal(img, re_img)

    def test_s5(self):
        img = np.array(np.random.rand(257, 257) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img)
        re_img = combine_square_img_boarder(metas)
        assert np.array_equal(img, re_img)

    def test_s5(self):
        img = np.array(np.random.rand(257, 257) * 255, dtype=np.uint8)
        metas = split_square_img_boarder(img,h=10,w=10,boarder=1)
        re_img = combine_square_img_boarder(metas,boarder=1)
        assert np.array_equal(img, re_img)




