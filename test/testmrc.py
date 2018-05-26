from mrc import Mrc as mrc
mrc1 = mrc.open('test_ffted.mrc')
print(mrc1.mrc.data.shape)
mrc1.writePng()
