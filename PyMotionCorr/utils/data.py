import arrayfire as af
import numpy as np
from ctypes import c_double, c_int
import ctypes


def af2np(data, _complex=False):
    data_c, dims = data.to_ctype(row_major=True, return_shape=True)
    new_dims = (dims[1], dims[0])
    if not _complex:
        return np.ctypeslib.as_array(data_c).reshape(new_dims).T
    else:
        print(type(ctypes.c_double * 2 * dims[0] * dims[1]))
        return np.frombuffer((ctypes.c_double * 2 * dims[0] * dims[1]).from_address(data_c), np.complex64).reshape(new_dims).T
        # np.frombuffer((ctypes.c_double * 2 * dims[0] * dims[1]).from_address(
        #     data_c), np.complex64).reshape(new_dims).T


def np2af(data, dtype=None):
    # return af.Array(data.ctypes.data, data.shape, data.dtype.char)
    print(type(data))
    if dtype:
        return af.Array(data.ctypes.data, data.shape, dtype)
    else:
        return af.Array(data.ctypes.data, data.shape, data.dtype.char)
