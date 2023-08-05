import operator

import cv2 as cv
import numpy as np
import pytest

from creevey.ops.image import centercrop, resize, trim_padding


class TestResize:
    def test_resize_validation(self, sample_image_square_rgb):
        with pytest.raises(ValueError):
            resize(sample_image_square_rgb, shape=(10, 10), min_dim=5)

    def test_resize_with_shape(self, sample_image_square_rgb):
        expected_shape = (5, 8)
        image = resize(sample_image_square_rgb, shape=expected_shape)
        actual_shape = image.shape[:2]
        assert actual_shape == expected_shape

    def test_resize_square_with_min_dim(self, sample_image_square_rgb):
        image = resize(sample_image_square_rgb, min_dim=50)
        actual_shape = image.shape[:2]
        expected_shape = (50, 50)
        assert actual_shape == expected_shape

    def test_resize_tall_with_min_dim(self, sample_image_tall_grayscale):
        image = resize(sample_image_tall_grayscale, min_dim=50)
        actual_shape = image.shape
        expected_shape = (68, 50)
        assert actual_shape == expected_shape

    def test_resize_wide_with_min_dim(self, sample_image_tall_grayscale):
        sample_image_wide = sample_image_tall_grayscale.transpose()
        image = resize(sample_image_wide, min_dim=50)
        actual_shape = image.shape
        expected_shape = (50, 68)
        assert actual_shape == expected_shape

    def test_resize_accepts_custom_reporting_args(self, sample_image_square_rgb):
        resize(sample_image_square_rgb, shape=(5, 8), inpath='fake', log_dict={})


class TestCenterCrop:
    def test_centercrop_square_rgb(self, sample_image_square_rgb):
        expected_shape = (16, 16, 3)
        actual_shape = centercrop(sample_image_square_rgb, reduction_factor=0.5).shape
        assert expected_shape == actual_shape

    def test_centercrop_tall_greyscale(self, sample_image_tall_grayscale):
        expected_shape = (17, 12)
        actual_shape = centercrop(
            sample_image_tall_grayscale, reduction_factor=0.5
        ).shape
        assert expected_shape == actual_shape

    def test_centercrop_square_rgba(self, sample_image_square_rgba):
        expected_shape = (16, 16, 4)
        actual_shape = centercrop(sample_image_square_rgba, reduction_factor=0.5).shape
        assert expected_shape == actual_shape

    def test_centercrop_reduction_factor(self, sample_image_square_rgb):
        expected_shape = (19, 19, 3)
        actual_shape = centercrop(sample_image_square_rgb, reduction_factor=0.6).shape
        assert expected_shape == actual_shape

    def test_centercrop_accepts_custom_reporting_args(self, sample_image_square_rgb):
        centercrop(
            sample_image_square_rgb, reduction_factor=0.5, inpath='fake', log_dict={}
        )


class TestTrimPadding:
    def test_trim_padding_no_padding(self, sample_image_square_rgb):
        image = trim_padding(
            sample_image_square_rgb, thresh=0.95, comparison_op=operator.gt
        )
        np.testing.assert_almost_equal(image, sample_image_square_rgb)

    def test_trim_padding_rgb(self, sample_image_square_rgb):
        im_padded = cv.copyMakeBorder(
            src=sample_image_square_rgb,
            top=np.random.randint(1, 100),
            bottom=np.random.randint(1, 100),
            left=np.random.randint(1, 100),
            right=np.random.randint(1, 100),
            borderType=cv.BORDER_CONSTANT,
            value=[251, 252, 253],
        )
        actual = trim_padding(im_padded, thresh=0.95, comparison_op=operator.gt)
        np.testing.assert_almost_equal(actual, sample_image_square_rgb)

    def test_trim_padding_rgba(self, sample_image_square_rgba):
        im_padded = cv.copyMakeBorder(
            src=sample_image_square_rgba,
            top=np.random.randint(1, 100),
            bottom=np.random.randint(1, 100),
            left=np.random.randint(1, 100),
            right=np.random.randint(1, 100),
            borderType=cv.BORDER_CONSTANT,
            value=[251, 252, 253],
        )
        actual = trim_padding(im_padded, thresh=0.95, comparison_op=operator.gt)
        np.testing.assert_almost_equal(actual, sample_image_square_rgba)

    def test_trim_padding_grayscale(self, sample_image_tall_grayscale):
        im_padded = cv.copyMakeBorder(
            src=sample_image_tall_grayscale,
            top=np.random.randint(1, 100),
            bottom=np.random.randint(1, 100),
            left=np.random.randint(1, 100),
            right=np.random.randint(1, 100),
            borderType=cv.BORDER_CONSTANT,
            value=251,
        )
        actual = trim_padding(im_padded, thresh=0.95, comparison_op=operator.gt)
        np.testing.assert_almost_equal(actual, sample_image_tall_grayscale)

    def test_trim_black_padding_rgb(self, sample_image_square_rgb):
        im_padded = cv.copyMakeBorder(
            src=sample_image_square_rgb,
            top=np.random.randint(1, 100),
            bottom=np.random.randint(1, 100),
            left=np.random.randint(1, 100),
            right=np.random.randint(1, 100),
            borderType=cv.BORDER_CONSTANT,
            value=3,
        )
        actual = trim_padding(im_padded, thresh=0.05, comparison_op=operator.lt)
        np.testing.assert_almost_equal(actual, sample_image_square_rgb)
