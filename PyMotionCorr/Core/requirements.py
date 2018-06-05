# -*- encoding:utf-8 -*-

import numpy as np
import arrayfire as af
# from numpy.fft import fft, ifft, fft2, ifft2, fftshift

# from scipy.signal import correlate2d
from numpy.fft import fft, fft2, ifft, ifft2, fftshift
from scipy.signal import fftconvolve
from scipy.signal import correlate2d
from numpy.linalg import lstsq, matrix_rank
from skimage.feature import register_translation
af.set_backend('cuda')