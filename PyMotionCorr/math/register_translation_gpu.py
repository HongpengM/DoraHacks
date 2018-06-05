try:
    from Core.requirements import *
    from utils.display import print_time
    from utils.data import np2af, af2np
except Exception as e:
    try:
        from ..Core.requirements import *
        from ..utils.display import print_time
        from ..utils.data import np2af, af2np
    except Exception as e:
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join('..', 'Core')))
        sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
        from requirements import *
        from display import print_time
        from utils.data import np2af, af2np
from skimage.feature.register_translation import _upsampled_dft

# def ifftshift()


def _upsampled_dft_af(data, upsampled_region_size,
                      upsample_factor=1, axis_offsets=None):
    """
    Upsampled DFT by matrix multiplication.
    This code is intended to provide the same result as if the following
    operations were performed:
        - Embed the array "data" in an array that is ``upsample_factor`` times
          larger in each dimension.  ifftshift to bring the center of the
          image to (1,1).
        - Take the FFT of the larger array.
        - Extract an ``[upsampled_region_size]`` region of the result, starting
          with the ``[axis_offsets+1]`` element.
    It achieves this result by computing the DFT in the output array without
    the need to zeropad. Much faster and memory efficient than the zero-padded
    FFT approach if ``upsampled_region_size`` is much smaller than
    ``data.size * upsample_factor``.
    Parameters
    ----------
    data : 2D afarray
        The input data array (DFT of original data) to upsample.
    upsampled_region_size : integer or tuple of integers, optional
        The size of the region to be sampled.  If one integer is provided, it
        is duplicated up to the dimensionality of ``data``.
    upsample_factor : integer, optional
        The upsampling factor.  Defaults to 1.
    axis_offsets : tuple of integers, optional
        The offsets of the region to be sampled.  Defaults to None (uses
        image center)
    Returns
    -------
    output : 2D afarray
            The upsampled DFT of the specified region.
    """
    # if people pass in an integer, expand it to a list of equal-sized sections
    if not hasattr(upsampled_region_size, "__iter__"):
        upsampled_region_size = [upsampled_region_size, ] * data.numdims()
    else:
        if len(upsampled_region_size) != data.numdims():
            raise ValueError("shape of upsampled region sizes must be equal "
                             "to input data's number of dimensions.")

    if axis_offsets is None:
        axis_offsets = [0, ] * data.numdims()
    else:
        if len(axis_offsets) != data.numdims():
            raise ValueError("number of axis offsets must be equal to input "
                             "data's number of dimensions.")
    # print_time('IFFT SHIFT')
    # print(np.fft.ifftshift(np.arange(data.shape[1]))[:, None])
    # print(np.fft.ifftshift(np.arange(data.shape[1]))[:, None].dtype.char)
    # print(np2af(np.fft.ifftshift(
    #     np.arange(data.shape[1]))[:, None], dtype='i'))
    # print_time('ARANGE')
    # print(np.arange(upsampled_region_size[1])[None, :])
    # print(np.arange(upsampled_region_size[1])[None, :].dtype)
    # print(np.arange(upsampled_region_size[1])[None, :].dtype.char)
    # print(np2af(np.arange(upsampled_region_size[1])[None, :], dtype='i'))

    # print('>>' * 20)
    # print(np2af(np.fft.ifftshift(
    #     np.arange(data.shape[1]))[:, None], dtype='i'))
    # print(np2af(np.fft.ifftshift(np.arange(data.shape[1]))[
    #       :, None], dtype='i') - np.floor(data.shape[1] / 2))
    # print(np2af(np.arange(upsampled_region_size[1])[
    #       None, :], dtype='i') - axis_offsets[1])
    # print('<<   ' * 20)
    print_time(np2af(np.fft.ifftshift(np.arange(data.shape[1]))[:, None], dtype='i') -
               np.floor(data.shape[1] / 2))
    print_time((np2af(np.arange(upsampled_region_size[1])[
        None, :], dtype='i') - axis_offsets[1]).as_type(af.Dtype.f64))
    print_time(axis_offsets)
    col_kernel = af.arith.exp((-1j * 2 * np.pi / (data.shape[1] * upsample_factor)) *
                              af.blas.matmul(np2af(np.fft.ifftshift(np.arange(data.shape[1]))[:, None], dtype='i') -
                                             np.floor(data.shape[1] / 2),
                                             (np2af(np.arange(upsampled_region_size[1])[None, :], dtype='i') -
                                              axis_offsets[1]).as_type(af.Dtype.f64))
                              )

    row_kernel = af.arith.exp((-1j * 2 * np.pi / (data.shape[0] * upsample_factor)) *
                              af.blas.matmul((np2af(np.arange(upsampled_region_size[0])[:, None], dtype='i') -
                                              axis_offsets[0]).as_type(af.Dtype.f64),
                                             np2af(np.fft.ifftshift(np.arange(data.shape[0]))[None, :], dtype='i') -
                                             np.floor(data.shape[0] / 2)
                                             )
                              )
    print_time(col_kernel.to_ctype())
    print_time(af2np(col_kernel, True))
    print_time(row_kernel)
    print_time(af2np(col_kernel, True))
    print_time(af2np(row_kernel), True)
    data = af2np(data)
    col_kernel = np.exp(
        (-1j * 2 * np.pi / (data.shape[1] * upsample_factor)) *
        (np.fft.ifftshift(np.arange(data.shape[1]))[:, None] -
         np.floor(data.shape[1] / 2)).dot(
             np.arange(upsampled_region_size[1])[None, :] - axis_offsets[1])
    )
    row_kernel = np.exp(
        (-1j * 2 * np.pi / (data.shape[0] * upsample_factor)) *
        (np.arange(upsampled_region_size[0])[:, None] - axis_offsets[0]).dot(
            np.fft.ifftshift(np.arange(data.shape[0]))[None, :] -
            np.floor(data.shape[0] / 2))
    )

    print_time(col_kernel)
    print_time(row_kernel)
    # col_kernel = np2af(col_kernel)
    # row_kernel = np2af(row_kernel)
    return
    return af.blas.matmul(af.blas.matmul(row_kernel, data), col_kernel)
