from PyMotionCorr.Core.requirements import *
af.set_backend('cuda')
print(fft(np.arange(16).reshape(4, 4)))
