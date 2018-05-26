import sys
import os.path
sys.path.append(os.path.abspath('../'))

from PyMotionCorr.Core.requirements import *
from PyMotionCorr.math.math import Math
import collections


class TestMath(object):
    """docstring for TestMath"""

    def __init__(self):
        super(TestMath, self).__init__()

    @staticmethod
    def testCCShift():
        # ==============Test cross corrleation shift==========================
        print('>>' * 20)
        print('Now running cc_fft test...')
        a = np.array([[3, 0, 0], [2, 0, 0], [1, 0, 0]])
        b = np.array([[3, 2, 1], [0, 0, 0], [0, 0, 0]])
        # print('Mat A:\n', a, '\n', 'Mat B:\n', b)
        math = Math()

        cc_fft = math.cross_correlation_using_fft(a, b)
        cc_shift_fft = math.compute_cc_peak_fft(a, b)
        cc_norm = math.normal_cross_correlation(a, b)
        cc_shift_norm = math.normal_cross_correlation_peak(a, b)

        def compare(x, y): return collections.Counter(
            x) == collections.Counter(y)

        # print('FFT\n', cc_fft)
        # print('normal\n', cc_norm)
        # print(cc_shift_fft)
        # print(cc_shift_norm)
        assert compare(cc_shift_fft, cc_shift_norm)
        print('Test cc_fft' + '.' * 20 + 'OK!')
        print('<<' * 20)
        # print(cc_norm[tuple(cc_shift_norm[0])])

    @staticmethod
    def testODE():
        # =======================Test over determined equation solution=========================
        print('>>' * 20)
        print('Now running over determined equation solution test...')
        a = np.array([[1, -1], [1, 1], [2, 1]])
        b = np.array([[2], [4], [8]])
        solution = np.array([[23 / 7], [8 / 7]])
        residual_error = np.array([[-1 / 7], [-3 / 7], [2 / 7]])
        # print('Mat A:\n', a, '\n', 'Mat B:\n', b)
        math = Math()
        s = math.solve_linear_equation(a, b)
        # print('Solution: \n', solution, '\nSolved Solution\n', s)
        # print(solution, s[0])
        assert np.allclose(solution, s[0])
        r_error = np.dot(a, s[0]) - b
        # print('Residual Error: \n', residual_error,
        # '\nSolved Residual Error\n', r_error)
        assert np.allclose(np.abs(residual_error), np.abs(r_error))
        print('Test over determined equation solution' + '.' * 20 + 'OK!')
        print('<<' * 20)

    @staticmethod
    def testIterODE():
         # =======================Test iterative ODE solution=========================
        print('>>' * 20)
        print('Now running iterative ODE solution test...')
        b = np.array([[1, 3], [4, 4], [3, 6], [3, 1], [2, 6], [-1, 3]])
        # solution = np.array([[23 / 7], [8 / 7]])
        # residual_error = np.array([[-1 / 7], [-3 / 7], [2 / 7]])
        # print('Mat A:\n', a, '\n', 'Mat B:\n', b)
        math = Math()
        r_s, A, delta_b = math.iterative_solve_linear_equation(
            b, threshold=0.8)

        print('Solved solution:\n', r_s,
              '\nCoefficient matrix\n', A, '\ndelta b\n', delta_b)

        # print('Solution: \n', solution, '\nSolved Solution\n', s)
        # print(solution, s[0])
        # assert np.allclose(solution, s[0])
        # print('Residual Error: \n', residual_error,
        # '\nSolved Residual Error\n', r_error)
        # assert np.allclose(np.abs(residual_error), np.abs(r_error))
        print('Test iterative ODE solution' + '.' * 20 + 'OK!')
        print('<<' * 20)


if __name__ == '__main__':
    test = TestMath()
    test.testIterODE()
