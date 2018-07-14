import sys
import os.path
sys.path.append(os.path.abspath('../'))
from PyMotionCorr.math.register_translation_gpu import _upsampled_dft_cu, register_translation_cu
from skimage.feature.register_translation import _upsampled_dft, register_translation
import numpy as np
import cupy as cp
from PyMotionCorr.utils.display import print_time
import unittest

from skimage.data import camera, binary_blobs
from scipy.ndimage import fourier_shift
from skimage import img_as_float
from skimage._shared import testing

from cupy.testing import assert_allclose, assert_array_almost_equal


def assertRaises(self, exc_type, func, *args, **kwargs):
    raised_exc = None
    try:
        func(*args, **kwargs)
    except exc_type as e:
        raised_exc = e
    if not raised_exc:
        self.fail("{0} was not raised".format(exc_type))


class TestRegisterTranslation(unittest.TestCase):
    """docstring for TestRegisterTranslation"""

    def testBasicMatOpr(self):
        # ==============Test arrayfire basic operation test==========================

        raw_data = np.arange(20).reshape(4, 5)
        raw_data_cp = cp.copy(raw_data)

        assert np.array_equal(raw_data, raw_data_cp)

    def testCudaUpsampleFFT(self):
        # ==============Test cuda version upsampling dft==========================

        raw_data = np.arange(1024 * 1024).reshape(1024, 1024)
        raw_data_cu = cp.arange(1024 * 1024).reshape(1024, 1024)
        # print(_upsampled_dft(raw_data, raw_data.shape))
        # print(_upsampled_dft_cu(raw_data_cu, raw_data_cu.shape))
        import time
        print(raw_data_cu.device)
        t0 = time.time()
        a = _upsampled_dft_cu(raw_data_cu, raw_data_cu.shape)
        t1 = time.time()
        b = _upsampled_dft(raw_data, raw_data.shape)
        t2 = time.time()
        print(t1 - t0, 's  ', t2 - t1, 's')

        from numpy.testing import assert_allclose
        assert_array_almost_equal(a, b)

    def test_correlation(self):

        reference_image = cp.fft.fftn(cp.array(camera()))
        shift = (-7, 12)
        reference_image_np = cp.asnumpy(reference_image)
        shifted_image = fourier_shift(reference_image_np, shift)
        shifted_image = cp.array(shifted_image)
        # pixel precision
        result, error, diffphase = register_translation_cu(reference_image,
                                                           shifted_image,
                                                           space="fourier")
        assert_allclose(result[:2], -cp.array(shift))

    def test_subpixel_precision(self):
        reference_image = cp.fft.fftn(cp.array(camera()))
        subpixel_shift = (-2.4, 1.32)
        reference_image_np = cp.asnumpy(reference_image)
        shifted_image = fourier_shift(reference_image_np, subpixel_shift)
        shifted_image = cp.array(shifted_image)
        # subpixel precision
        result, error, diffphase = register_translation_cu(reference_image,
                                                           shifted_image, 100,
                                                           space="fourier")
        assert_allclose(result[:2], -cp.array(subpixel_shift), atol=0.05)

    def test_real_input(self):
        reference_image = cp.array(camera())
        subpixel_shift = (-2.4, 1.32)
        shifted_image = fourier_shift(
            cp.asnumpy(cp.fft.fftn(reference_image)), subpixel_shift)
        shifted_image = cp.fft.ifftn(cp.array(shifted_image))

        # subpixel precision
        result, error, diffphase = register_translation_cu(reference_image,
                                                           shifted_image, 100)
        assert_allclose(result[:2], -cp.array(subpixel_shift), atol=0.05)

    def test_size_one_dimension_input(self):
        # take a strip of the input image
        reference_image = cp.fft.fftn(
            cp.array(camera())[:, 15]).reshape((-1, 1))
        subpixel_shift = (-2.4, 4)

        shifted_image = fourier_shift(
            cp.asnumpy(reference_image), subpixel_shift)
        shifted_image = cp.array(shifted_image)
        # subpixel precision
        result, error, diffphase = register_translation_cu(reference_image,
                                                           shifted_image, 100,
                                                           space="fourier")
        assert_allclose(result[:2], -cp.array((-2.4, 0)), atol=0.05)

    def test_3d_input(self):
        phantom = cp.array(img_as_float(binary_blobs(length=32, n_dim=3)))
        reference_image = cp.fft.fftn(phantom)
        shift = (-2., 1., 5.)
        shifted_image = fourier_shift(cp.asnumpy(reference_image), shift)
        shifted_image = cp.array(shifted_image)
        result, error, diffphase = register_translation_cu(reference_image,
                                                           shifted_image,
                                                           space="fourier")
        assert_allclose(result, -cp.array(shift), atol=0.05)
        # subpixel precision not available for 3-D data
        subpixel_shift = (-2.3, 1., 5.)
        shifted_image = fourier_shift(
            cp.asnumpy(reference_image), subpixel_shift)
        shifted_image = cp.array(shifted_image)
        result, error, diffphase = register_translation_cu(reference_image,
                                                           shifted_image,
                                                           space="fourier")
        assert_allclose(result, -cp.array(shift), atol=0.5)
        with self.assertRaises(NotImplementedError):
            register_translation_cu(
                reference_image,
                shifted_image, upsample_factor=100,
                space="fourier")

    def test_unknown_space_input(self):
        image = cp.ones((5, 5))
        with self.assertRaises(ValueError):
            register_translation_cu(
                image, image,
                space="frank")

    def test_wrong_input(self):
        # Dimensionality mismatch
        image = cp.ones((5, 5, 1))
        template = cp.ones((5, 5))
        with self.assertRaises(ValueError):
            register_translation_cu(template, image)

        # Greater than 2 dimensions does not support subpixel precision
        #   (TODO: should support 3D at some point.)
        image = cp.ones((5, 5, 5))
        template = cp.ones((5, 5, 5))
        with self.assertRaises(NotImplementedError):
            register_translation_cu(template, image, 2)

        # Size mismatch
        image = cp.ones((5, 5))
        template = cp.ones((4, 4))
        with self.assertRaises(ValueError):
            register_translation_cu(template, image)

    def test_mismatch_upsampled_region_size(self):
        with self.assertRaises(ValueError):
            _upsampled_dft_cu(
                cp.ones((4, 4)),
                upsampled_region_size=[3, 2, 1, 4])

    def test_mismatch_offsets_size(self):
        with self.assertRaises(ValueError):
            _upsampled_dft_cu(cp.ones((4, 4)), 3,
                              axis_offsets=[3, 2, 1, 4])


if __name__ == '__main__':
    test = TestRegisterTranslation()
    # test.testBasicMatOpr()
    # test.testCudaUpsampleFFT()
    # test.testCudaRT()
    unittest.main()
