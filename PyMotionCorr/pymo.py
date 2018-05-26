from ..mrc import Mrc as mrc
import numpy as np
from tqdm import tqdm


class MotionCorr(object):
    """docstring for MotionCorr"""

    def __init__(self):
        super(MotionCorr, self).__init__()
        pass

    def a():
        pass


if __name__ == '__main__':
    '''
     mrcf = mrc.open('test.mrc')
    # print(mrcf)
    print(mrcf.imageShape)
    print(mrcf.frameNums)

    # --------Crop img for fft--------
    croppedShape = min(mrcf.imageShape)
    if croppedShape % 2 != 0:
        croppedShape -= 1
    croppedShape = (croppedShape,) * 2
    cropped_mrc = np.zeros((mrcf.frameNums,) + croppedShape, dtype=np.float32)
    print(mrcf.filehandle[:-4])
    print(mrcf.filename)
    print(croppedShape)
    print('Image Start Cropping')
    for i in tqdm(range(mrcf.frameNums), ncols=60):
        cropped_mrc[i] = mrcf[i, 0:croppedShape[0], 0:croppedShape[1]]
    print('Crop Finished, Now writing to cropped mrc...')
    mrc.write(mrcf.filename + '_cropped_2.mrc',
              cropped_mrc[0:3], mrcfh=mrcf.filehandle)
    print('Fininshed writing to disk')
    '''

    # -----------------------------
    #****** Small memory test******
    # -----------------------------

    '''
    mrcf = mrc.open('test.mrc')
    # print(mrcf)
    print(mrcf.imageShape)
    print(mrcf.frameNums)

    # --------Crop img for fft--------
    croppedShape = min(mrcf.imageShape)
    if croppedShape % 2 != 0:
        croppedShape -= 1
    croppedShape = (croppedShape,) * 2
    cropped_mrc = np.zeros((mrcf.frameNums,) + croppedShape, dtype=np.float32)
    print(mrcf.filehandle[:-4])
    print(mrcf.filename)
    print(croppedShape)
    print('Image Start Cropping')
    for i in tqdm(range(3), ncols=60):
        cropped_mrc[i] = mrcf[i, 0:croppedShape[0], 0:croppedShape[1]]
    print('Crop Finished, Now writing to cropped mrc...')
    mrc.write(mrcf.filename + '_cropped_2.mrc',
              cropped_mrc[0:3], mrcfh=mrcf.filehandle)
    print('Fininshed writing to disk')
    '''

    # -------Do fft on Cropped img-------
    cropped_mrc = mrc.open('test_cropped_2.mrc')
    ffted_mrc = np.zeros(cropped_mrc.mrc.data.shape, dtype=np.complex64)
    print(cropped_mrc.imageShape, ffted_mrc.shape
          )
    print(cropped_mrc.getFilename(origin=True))
    print('-' * 10 + 'Image Start Doing FFT' + '-' * 10)
    for i in tqdm(range(cropped_mrc.frameNums), ncols=60):
        ffted_mrc[i] = np.fft.fft2(cropped_mrc[i])
    mrc.write(cropped_mrc.getFilename(origin=True) + '_ffted_2.mrc',
              ffted_mrc, mrcfh=cropped_mrc.filehandle)
    print('-' * 10 + 'Fininshed writing to disk' + '-' * 10)

    # --------Find fft shift--------------

    #  # ------------Find best cc using fft -----------

    # ffted_mrc = np.zeros(mrcf.data.shape)
    # for i in range(len(mrc.frameNums)):
    #     ffted_mrc[i] = np.fft.fft2()
