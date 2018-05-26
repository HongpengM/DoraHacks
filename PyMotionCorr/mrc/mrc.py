import mrcfile
import numpy as np
import copy
import os
import scipy.misc as misc
from skimage.exposure import rescale_intensity
from tqdm import tqdm


class Mrc(object):
    """docstring for mrc"""

    def __init__(self, filehandle, validate=False):
        '''
            This initialize function only open .mrc file with 
            mmap read-only
        '''
        super(Mrc, self).__init__()
        self.filehandle = filehandle
        self.mrc = mrcfile.mmap(filehandle, mode='r')
        if validate:
            print('*' * 20 + 'Validating start' + '*' * 20)
            if not mrcfile.validate(filehandle):
                raise ValueError('Initial Mrc File is not validated')
            print('*' * 20 + 'Validating finished' + '*' * 20)
        '''
        self.header = self.mrc.header
        self.exheader = self.mrc.extended_header
        self.volsize = self.mrc.voxel_size
        # self.rawdata Raw data From .mrc file
        self.rawdata = np.copy(self.mrc.data)
        '''

    @property
    def imageShape(self):
        '''
        Return image shape
        '''
        if len(self.mrc.data.shape) == 2:
            return self.mrc.data.shape
        elif len(self.mrc.data.shape) == 3:
            return self.mrc.data.shape[1:]
        else:
            raise ValueError('Cannot get mrc file shape')

    @property
    def frameNums(self):
        '''
        Return Frame numbers
        '''
        if len(self.mrc.data.shape) == 2:
            return 1
        elif len(self.mrc.data.shape) == 3:
            return self.mrc.data.shape[0]

    @property
    def _writable(self):
        return self.mrc._check_writable()

    @property
    def copydata(self):
        return np.copy(self.mrc.data)

    @property
    def filename(self):
        return self.getFilename()

    def getFilename(self, origin=False):
        if origin:
            if self.filehandle.find('_'):
                return self.filehandle[:self.filehandle.find('_')]
            else:
                return self.filehandle[:self.filehandle.find('.')]
        else:
            return self.filehandle[:self.filehandle.find('.')]

    def writePng(self, frame_i=None, scaleFactor=10):
        new_shape = (int(self.imageShape[0] / scaleFactor),
                     int(self.imageShape[1] / scaleFactor))
        imgPath = self.filename + '_png'
        if not os.path.isdir(imgPath):
            os.mkdir(imgPath)
        # Write all frames to png
        if not frame_i:
            print('Writing Png Img...')
            for i in tqdm(range(self.frameNums), ncols=60):
                frame_i_data = rescale_intensity(
                    misc.imresize(self.frame(i), new_shape))
                misc.imsave(os.path.join(imgPath, self.filename +
                                         '_' + str(i) + '.png'),
                            frame_i_data)
            print('Writing Png Img Finished')
        # Write specific frame to png
        else:
            print('Writing ' + str(frame_i) + ' Png Img...')
            frame_i_data = frame_i_data = rescale_intensity(
                misc.imresize(self.frame(i), new_shape))
            misc.imsave(os.path.join(imgPath, self.filename +
                                     '_' + str(frame_i) + '._png'),
                        frame_i_data)
            print('Writing Png Img Finished')
        return frame_i_data

    @classmethod
    def open(cls, filepath):
        mrcf = Mrc(filepath)
        return mrcf

    @classmethod
    def write(cls, filename, data, filepath=None,
              mrcfh=None, exheader=None):
        '''
        Return writed mrc filehandle
        -------------------------------
        This class method write will write an 
        mrcfile by copy parameters
        from existing mrc or mannually input
        '''
        print(mrcfh)

        if filepath == None:
            filepath = os.getcwd()
        if not (mrcfh or exheader):
            raise ValueError('Not enough parameters to \
             write mrcfile')
        if exheader:
            pass
        else:
            _mrc = mrcfile.mmap(mrcfh)
            # header = _mrc.header
            exheader = _mrc.extended_header
            # volsize = _mrc.voxel_size
            _mrc.close()

        filehandle = os.path.join(filepath, filename)
        with mrcfile.new(filehandle) as mrc:
            mrc.set_data(data)
            # print(mrc._check_writeable())
            # mrc._set_voxel_size(volsize)
            mrc.set_extended_header(exheader)
        return filehandle

    def frame(self, i):
        if self.frameNums > 1:
            return self.mrc.data[i]
        else:
            raise ValueError(
                'This mrc file is not an image stack file,\
                 cannot get frame data')

    def image(self, i):
        if self.__ImgStack__:
            return self.mrc.data[i]
        else:
            return self.mrc.data

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.frame(key)
        else:
            return self.mrc.data[key]

    def readImagePixel(self, nImage, nX, nY):
        return self.rawdata[nImage, nX, nY]

    def __repr__(self):
        reprtxt = ''
        for item in self.mrc.header.dtype.names:
            reprtxt += str(item) + ': ' + \
                str(self.mrc.header[item]) + '\n'
        # reprtxt += str(self.mrc.data)
        return reprtxt


if __name__ == '__main__':
    mrcf = Mrc.open('test.mrc')
    print(mrcf)
    print(mrcf.mrc.data.shape)
    # print(mrcf._check_writeable())
    print(mrcf[0:2].shape)
    print(mrcf.filehandle)
    Mrc.write('test3.mrc', np.copy(mrcf[0:2]),
              mrcfh=mrcf.filehandle)
    mrcnew = Mrc.open('test3.mrc')
    print(mrcnew)
