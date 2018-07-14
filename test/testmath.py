import sys
import os.path
sys.path.append(os.path.abspath('../'))

from PyMotionCorr.Core.requirements import *
from PyMotionCorr.math.math import Math
import collections
import unittest
from numpy.testing import assert_allclose, assert_almost_equal


class TestMath(unittest.TestCase):
    """
    Unit test of math.py
    """

    def testCCShift(self):
        # ==============Test cross corrleation shift==========================

        a = np.array([[3, 0, 0], [2, 0, 0], [1, 0, 0]])
        b = np.array([[3, 2, 1], [0, 0, 0], [0, 0, 0]])
        math = Math()
        cc_fft = math.cross_correlation_using_fft(a, b)
        cc_shift_fft = math.compute_cc_peak_fft(a, b)
        cc_norm = math.normal_cross_correlation(a, b)
        cc_shift_norm = math.normal_cross_correlation_peak(a, b)

        def compare(x, y): return collections.Counter(
            x) == collections.Counter(y)
        assert compare(cc_shift_fft, cc_shift_norm)

    def testODE(self):
        # =======================Test over determined equation solution=========================
        a = np.array([[1, -1], [1, 1], [2, 1]])
        b = np.array([[2], [4], [8]])
        solution = np.array([[23 / 7], [8 / 7]])
        residual_error = np.array([[-1 / 7], [-3 / 7], [2 / 7]])
        math = Math()
        s = math.solve_linear_equation(a, b)
        assert np.allclose(solution, s[0])
        r_error = np.dot(a, s[0]) - b
        assert np.allclose(np.abs(residual_error), np.abs(r_error))

    def testIterODE(self):
         # =======================Test iterative ODE solution=========================

        b = np.array([[1, 3], [4, 4], [3, 6], [3, 1], [2, 6], [-1, 3]])

        math = Math()
        r_s, A, delta_b = math.iterative_solve_linear_equation(
            b, threshold=0.8)
        assert_almost_equal(delta_b, np.zeros(delta_b.shape))
        # print('Solved solution:\n', r_s,
        #       '\nCoefficient matrix\n', A, '\ndelta b\n', delta_b)


if __name__ == '__main__':
    unittest.main()
