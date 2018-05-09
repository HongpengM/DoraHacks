from mrc import Mrc as mrc
mrc1 = mrc.open('test_cropped.mrc')
print(mrc1.mrc.data.shape)
mrc1.writePng()
