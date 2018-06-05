from PyMotionCorr.Core.requirements import *
from PyMotionCorr.mrc.mrc import Mrc as mrc
from PyMotionCorr.math.math import Math
import pickle
from time import gmtime, strftime

math = Math()
mrc1 = mrc.open('data\\test_cropped.mrc')
print(mrc1.mrc.data.shape)
frame_num = mrc1.mrc.data.shape[0]
counter = 0
pkl_save_file = open('offset.pickle', 'wb')
offset_list = []
for i in range(frame_num):
    for j in range(i):
        counter += 1
        print('[', strftime("%Y-%m-%d %H:%M:%S", gmtime()), ']',
              'No.', counter, ', Pair: ', j, i)
        cc_offset = math.cc_upsample(mrc1.frame(j), mrc1.frame(i))
        print(cc_offset)
        offset_list.append([counter, j, i,
                            cc_offset[0], cc_offset[1], cc_offset[2]])

pickle.dump(offset_list, pkl_save_file, protocol=pickle.HIGHEST_PROTOCOL)
pkl_save_file.close()
