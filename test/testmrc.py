
import sys
import os.path
sys.path.append(os.path.abspath('../'))
from PyMotionCorr.Core.requirements import *
from PyMotionCorr.mrc.mrc import Mrc as mrc


class TestMrc(object):
    """docstring for TestMrc"""

    def __init__(self):
        super(TestMrc, self).__init__()

    @staticmethod
    def testOpenMrc():
        # ==============Test mrc open==========================
        print('>>' * 20)
        print('Now running mrc open test...')
        mrc1 = mrc.open('..\\data\\test.mrc')
        print(mrc1.mrc.data.shape)
        assert mrc1.mrc.data.shape == (38, 7676, 7420)
        print('Test mrc open' + '.' * 20 + 'OK!')
        print('<<' * 20)
        mrc1.writePng()


if __name__ == '__main__':
    test = TestMrc()
    test.testOpenMrc()
