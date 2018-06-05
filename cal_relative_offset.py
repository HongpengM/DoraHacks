from PyMotionCorr.Core.requirements import *
from PyMotionCorr.math.math import Math
import pickle
with open('offset.pickle', 'rb') as hdl:
    abs_offset = pickle.load(hdl)
b_len = len(abs_offset)
b = np.zeros((b_len, 2))
for i in range(b_len):
    b[i] = abs_offset[i][3]
print(b.shape)
math = Math()
r_s, A, delta_b = math.iterative_solve_linear_equation(b)
print('Solution', r_s)
print('Delta b', delta_b)
r_s, A, delta_b = math.solve_linear_equation_once(b)
print('Solution', r_s)
print('Delta b', delta_b)
