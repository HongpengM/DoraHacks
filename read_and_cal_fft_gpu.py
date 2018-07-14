from PyMotionCorr.Core.requirements import *
from PyMotionCorr.mrc.mrc import Mrc as mrc
from PyMotionCorr.math.math import Math
import pickle
from PyMotionCorr.utils.display import print_time
import cupy as cp


math = Math()
mrc1 = mrc.open('data\\test_cropped.mrc')
print(mrc1.mrc.data.shape)
frame_num = mrc1.mrc.data.shape[0]
print(type(mrc1.mrc.data[0]))
mrc_data = np.array(mrc1.mrc.data[0])
test_data = af.Array(mrc_data.ctypes.data, mrc_data.shape, mrc_data.dtype.char)
print(test_data.shape)
print_time()

print(af.signal.fft2(test_data)[:1, :10])
print_time()
print_time()
print(np.fft.fft2(mrc_data)[:10, :1])

print_time()
