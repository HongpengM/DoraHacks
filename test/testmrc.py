
import sys
import os.path
sys.path.append(os.path.abspath('../'))
from PyMotionCorr.Core.requirements import *
from PyMotionCorr.mrc.mrc import Mrc as mrc
import unittest


class TestMrc(unittest.TestCase):
    """docstring for TestMrc"""

    @staticmethod
    def testOpenMrc():
        # ==============Test mrc open==========================

        mrc1 = mrc.open('..\\data\\test.mrc')
        assert mrc1.mrc.data.shape == (38, 7676, 7420)


if __name__ == '__main__':
    unittest.main()
