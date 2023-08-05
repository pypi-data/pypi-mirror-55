from lailib.image.convert import *
import numpy as np
import os
import cv2


class TestBase64:
    def test_acc_base64_color(self, tmpdir):
        img_rgb = np.array(np.random.rand(128,256,3)*255,dtype=np.uint8)
        img_path = os.path.join(tmpdir,"test_color.png")
        cv2.imwrite(img_path,img_rgb)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str)
        assert img_from_str.shape == img_rgb.shape
        assert np.array_equal(img_from_str,img_rgb)


    def test_acc_base64_gray(self, tmpdir):
        img = np.array(np.random.rand(128,256)*255,dtype=np.uint8)
        img_path = os.path.join(tmpdir,"test_color.png")
        cv2.imwrite(img_path,img)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str,rgb=False)
        assert img_from_str.shape == img.shape
        assert np.array_equal(img_from_str,img)

    def test_acc_base64_color_xl(self, tmpdir):
        img_rgb = np.array(np.random.rand(4000,4000,3)*255,dtype=np.uint8)
        img_path = os.path.join(tmpdir,"test_color.png")
        cv2.imwrite(img_path,img_rgb)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str)
        assert img_from_str.shape == img_rgb.shape
        assert np.array_equal(img_from_str,img_rgb)


    def test_acc_base64_gray_xl(self, tmpdir):
        img = np.array(np.random.rand(4000,4000)*255,dtype=np.uint8)
        img_path = os.path.join(tmpdir,"test_color.png")
        cv2.imwrite(img_path,img)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str,rgb=False)
        assert img_from_str.shape == img.shape
        assert np.array_equal(img_from_str,img)

    def test_acc_base64_color_xs(self, tmpdir):
        img_rgb = np.array(np.random.rand(2,2,3)*255,dtype=np.uint8)
        img_path = os.path.join(tmpdir,"test_color.png")
        cv2.imwrite(img_path,img_rgb)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str)
        assert img_from_str.shape == img_rgb.shape
        assert np.array_equal(img_from_str,img_rgb)


    def test_acc_base64_gray_xs(self, tmpdir):
        img = np.array(np.random.rand(2,2)*255,dtype=np.uint8)
        img_path = os.path.join(tmpdir,"test_color.png")
        cv2.imwrite(img_path,img)
        base64_str = base64_from_file(img_path)
        img_from_str = base64_to_img(base64_str,rgb=False)
        assert img_from_str.shape == img.shape
        assert np.array_equal(img_from_str,img)