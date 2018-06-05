import sys
import os.path
sys.path.append(os.path.abspath('../'))
from PyMotionCorr.math.register_translation_gpu import _upsampled_dft_af
from skimage.feature.register_translation import _upsampled_dft
import numpy as np
import arrayfire as af
from PyMotionCorr.utils.display import print_time
from PyMotionCorr.utils.data import af2np


class TestRegisterTranslation(object):
    """docstring for TestRegisterTranslation"""

    def __init__(self):
        super(TestRegisterTranslation, self).__init__()

    @staticmethod
    def testBasicMatOpr():
        # ==============Test arrayfire basic operation test==========================
        print('>>' * 20)
        print('Now running arrayfire basic operation test...')
        raw_data = np.arange(20).reshape(4, 5)
        raw_data_af = af.interop.from_ndarray(raw_data)
        print_time(raw_data)
        print_time(raw_data_af)
        print_time(af2np(raw_data_af))
        print_time(af2np(raw_data_af).reshape((5, 4)).T)
        assert np.array_equal(raw_data, af2np(raw_data_af))
        print('Test arrayfire basic operation' + '.' * 20 + 'OK!')
        print('<<' * 20)

    @staticmethod
    def testCtypes2Numpy():
        # ==============Test arrayfire basic operation test==========================
        print('>>' * 20)
        print('Now running arrayfire basic operation test...')
        raw_data = np.arange(20, dtype=np.complex64).reshape(4, 5)
        raw_data_af = af.interop.from_ndarray(raw_data)
        raw_data_c, dims = raw_data_af.to_ctype(
            row_major=True, return_shape=True)
        print(raw_data)
        print(raw_data_af)
        print(raw_data_af.to_array())
        print(raw_data_c)
        import ctypes
        np.frombuffer(np.core.multiarray.int_asbuffer(
            ctypes.addressof(raw_data_c), int(dims[0] * dims[1]) * np.dtype(float).itemsize))
        print('Test arrayfire version upsampling dft' + '.' * 20 + 'OK!')
        print('<<' * 20)

    @staticmethod
    def testAfRT():
        # ==============Test arrayfire version upsampling dft==========================
        print('>>' * 20)
        print('Now running arrayfire version upsampling dft test...')
        raw_data = np.arange(64).reshape(8, 8)
        raw_data_af = af.interop.from_ndarray(raw_data)
        # print(_upsampled_dft(raw_data, raw_data.shape))
        print(_upsampled_dft_af(raw_data_af, raw_data_af.shape))

        print('Test arrayfire version upsampling dft' + '.' * 20 + 'OK!')
        print('<<' * 20)


if __name__ == '__main__':
    test = TestRegisterTranslation()
    # test.testBasicMatOpr()
    # test.testAfRT()
    test.testCtypes2Numpy()
