try:
    from Core import requirements
except Exception as e:
    from ..Core import requirements
import numpy as np
from numpy.fft import fft, fft2, ifft, ifft2, fftshift
from scipy.signal import fftconvolve
from scipy.signal import correlate2d
from numpy.linalg import lstsq, matrix_rank
from skimage.feature import register_translation


class Math(object):
    """docstring for Math"""

    def __init__(self):
        super(Math, self).__init__()

    @staticmethod
    def cc_upsample(x, y_offset):
        shift, error, diffphase = register_translation(x, y_offset, 32)
        return shift, error, diffphase

    @staticmethod
    def cross_correlation_using_fft(x, y):

        return fftconvolve(x, y[::-1, ::-1], mode='same')

    # shift < 0 means that y starts 'shift' time steps before x
    # shift > 0 means that y starts 'shift' time steps after x

    @staticmethod
    def compute_cc_peak_fft(x, y):
        c = Math.cross_correlation_using_fft(x, y)
        return np.argwhere(c == np.max(c))[0]

    @staticmethod
    def normal_cross_correlation(x, y):
        return correlate2d(x, y, mode='same')

    @staticmethod
    def normal_cross_correlation_peak(x, y):
        mat = Math.normal_cross_correlation(x, y)
        return np.argwhere(mat == np.max(mat))[0]

    @staticmethod
    def solve_linear_equation(a, b):
        return lstsq(a, b)

    @staticmethod
    def solve_linear_equation_once(b):
        n = b.shape[0] * 2
        n = int(np.sqrt(n))
        n = np.max([n, int(b.shape[0] * 2 / n)])
        m = int(n * (n - 1) / 2)
        # Initial step: Get coefficient matrix
        A = Math.initial_coeff_matrix(n)
        assert A.shape[0] == b.shape[0]
        r_s = lstsq(A, b)[0]

        r_error = np.dot(A, r_s) - b
        delta_b = np.zeros((r_error.shape[0],))
        for i in range(len(delta_b)):
            delta_b[i] = np.sqrt(r_error[i, 0] ** 2 + r_error[i, 1] ** 2)
        return r_s, A, delta_b

    @staticmethod
    def iterative_solve_linear_equation(b, threshold=1):
        '''
        Iteratively Solve: A * r_s = b
                           delta_b = || A * r_s  - b ||
        Filter by residual error delta_b
        :return: 
            squared least solution r_s
        '''
        # Initial step: Get (#r_adjacent)
        n = b.shape[0] * 2
        n = int(np.sqrt(n))
        n = np.max([n, int(b.shape[0] * 2 / n)])
        m = int(n * (n - 1) / 2)
        # Initial step: Get coefficient matrix
        A = Math.initial_coeff_matrix(n)
        assert A.shape[0] == b.shape[0]
        r_s = lstsq(A, b)[0]

        r_error = np.dot(A, r_s) - b
        delta_b = np.zeros((r_error.shape[0],))
        for i in range(len(delta_b)):
            delta_b[i] = np.sqrt(r_error[i, 0] ** 2 + r_error[i, 1] ** 2)
        flag_full_rank = True
        flag_not_convergence = (len(np.argwhere(delta_b > threshold)) > 0)
        while flag_full_rank and flag_not_convergence:

            # Select outlier by residual error > threshold
            outlier = np.argwhere(delta_b > threshold)
            total_outlier = len(outlier)
            # Set new A, b
            A_new = np.zeros((m - total_outlier, n - 1))
            b_new = np.zeros((m - total_outlier, b.shape[1]))
            for i in range(total_outlier + 1):
                if i == 0:
                    A_new[:outlier[i][0]] = A[:outlier[i][0]]
                    b_new[:outlier[i][0]] = b[:outlier[i][0]]
                if i == total_outlier:
                    A_new[outlier[i - 1][0] + 1 -
                          i:] = A[outlier[i - 1][0] + 1:]
                    b_new[outlier[i - 1][0] + 1 -
                          i:] = b[outlier[i - 1][0] + 1:]
                else:
                    A_new[outlier[i - 1][0] + 1 - i:outlier[i][0] - i
                          ] = A[outlier[i - 1][0] + 1:outlier[i][0]]
                    b_new[outlier[i - 1][0] + 1 - i:outlier[i][0] - i
                          ] = b[outlier[i - 1][0] + 1:outlier[i][0]]
                # print('Updated coefficient matrix\n', A_new)
            # ====If not full rank, solve ODE is impossible
            flag_full_rank = (matrix_rank(A_new) == n - 1)
            if not flag_full_rank:
                break
            A = A_new
            b = b_new
            r_s = lstsq(A, b)[0]
            r_error = np.dot(A, r_s) - b
            delta_b = np.zeros((r_error.shape[0],))
            for i in range(len(delta_b)):
                delta_b[i] = np.sqrt(r_error[i, 0] ** 2 + r_error[i, 1] ** 2)
            # if convergence, no need to go further
            flag_not_convergence = (len(np.argwhere(delta_b > threshold)) > 0)

            # print(outlier)
            # print(total_outlier)
            # print('Updated coefficient matrix\n', A_new)
            # print(A)
            # print('Updated b\n', b_new)
            # print(b)
            # print(matrix_rank(A))

        return r_s, A, delta_b

    @staticmethod
    def initial_coeff_matrix(n):
        m = int(n * (n - 1) / 2)
        cnt = 0
        cnt2 = 0
        coeff = np.zeros((m, n - 1))
        for i in range(n):
            for j in range(i + 1, n, 1):
                # print(i, j)
                for k in range(i, j, 1):
                    coeff[cnt, k] = 1
                    # print(i, j, k)
                    # print(i * n + j)
                cnt += 1
        # print(m, cnt)
        # print(coeff)
        return coeff


if __name__ == '__main__':
    a = np.arange(121).reshape(11, 11)
    b = np.arange(121).reshape(11, 11) - np.eye(11)
