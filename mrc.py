import mrcfile
import numpy as np
import copy


class mrc(object):
    """docstring for mrc"""

    def __init__(self, filepath, mode='r'):
        super(mrc, self).__init__()
        self.filepath = filepath
        self.mode = mode
        self.mrc = mrcfile.mmap(filepath, mode)

    def _check_writeable(self):
        return self.mrc._check_writeable()

    @classmethod
    def open(cls, filepath, mode='r'):
        print(filepath, mode)
        mrcf = mrc(filepath, mode=mode)
        return mrcf

    def close(self):
        self.mrc.close()

    def flush(self):
        self.mrc.flush()

    def data(self):
        return self.mrc.data

    def is_image_stack(self):
        return self.mrc.is_image_stack()

    def is_single_image(self):
        return self.mrc.is_single_image()

    def readImagePixel(self, nImage, nX, nY):
        return self.mrc[nImage, nX, nY]

    def image(self, nImage):
        if self.is_image_stack():
            return self.mrc.data[nImage]
        elif nImage == 0:
            return self.mrc.data
        else:
            raise AttributeError('Select image no. in non-stack data')

    def wirteImageData(self, arr, nImage, nX, nY):
        self._check_writeable()
        newdata = np.copy(self.mrc.data)
        newdata[nImage, nX:nX + arr.shape[0], nY:nY + arr.shape[1]] = arr
        return self.mrc.set_data(newdata)

    def __repr__(self):
        reprtxt = ''
        for item in self.mrc.header.dtype.names:
            reprtxt += str(item) + ': ' + str(self.mrc.header[item]) + '\n'
        # reprtxt += str(self.mrc.data)
        return reprtxt


if __name__ == '__main__':
    mrcf = mrc.open('test.mrc', 'r')
    print(mrcf)
    print(mrcf.is_image_stack())
    print(mrcf.mrc.data.shape)
    print(mrcf._check_writeable())
