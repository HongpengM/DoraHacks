from mrc import Mrc as mrc
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
    mrc.write(mrcf.filename + '_cropped.mrc',
              cropped_mrc, mrcfh=mrcf.filehandle)
    print('Fininshed writing to disk')

    #

    # ffted_mrc = np.zeros(mrcf.data.shape)
    # for i in range(len(mrc.frameNums)):
    #     ffted_mrc[i] = np.fft.fft2()
