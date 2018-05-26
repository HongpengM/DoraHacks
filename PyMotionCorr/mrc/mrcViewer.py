import numpy as np
import mrcfile
import h5py
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2

frame_path = '14sep05c_00024sq_00003hl_00002es.frames.mrc'
norm_path = 'norm-amibox05-0.mrc'


def readArrayMrc(mrc):
    '''
    Open and return mrc file data part
    '''
    with mrcfile.open(mrc) as mrc:
        # mrc.print_header()
        return mrc.data


def demoArrDataCV(frame, norm=None, args='Sample.jpg'):
    '''
    Show mrc image.
    Input: frame /  frame + norm
        args: image name to be saved 

    Press 'Esc' to end demo
    '''
    if norm != None:
        data = np.multiply(frame, norm)
    else:
        data = frame
    data = (data - data.min()) / data.mean() * 255

    print('OpenCV demo image')
    print(data)
    print(data.shape)
    cv2.imwrite('./data.png', data)
    data = cv2.imread('./data.png', 0)
    # cl1 = cv2.equalizeHist(data)
    # map = np.zeros((3710,3710,1), np.uint8)
    # out = cv2.distanceTransform(data, cv2.DIST_LABEL_CCOMP, 3, map)
    # dst = threshed
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(data)
    data = np.array(cl1)

    cv2.imwrite(args, data)
    cv2.imshow('Color image', data)
    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            break
        # elif k == ord('s'):  # wait for 's' key to save and exit
        #     cv2.imwrite(args, data)
    return
    cv2.destroyAllWindows()


def demoArrayData(frame, norm=None, args='Sample.png'):
    '''
    Depricated
    '''
    if norm != None:
        data = np.multiply(frame, norm)
    else:
        data = frame

    data = (data - data.min()) / (data.max() - data.min()) * 255
    fig = plt.figure()
    img = plt.imshow(data, vmin=data.min(), vmax=data.max(), cmap='gray')
    fig.savefig(args)


def overlayFramesNorm(frames, norm, mode=2):
    '''
    Overlay Frames without adjustment, and there is 3 mode of norm
    Mode:
        0: no normalization
        1: directly normalization
        2: normalization with norm matrix flipped vertically
    '''
    frame_num = frames.shape[0]
    result_mat = np.zeros(norm.shape)
    for i in range(frame_num):
        fr = frames[i]
        result_mat += fr
    result_mat /= frame_num
    if mode == 0:
        return result_mat
    elif mode == 1:
        return np.multiply(result_mat, norm)
    elif mode == 2:
        return np.multiply(result_mat, np.flip(norm, 0))


def overlayFrames(frames):
    '''
    Overlay frames without adjustment and normalization
    '''
    frame_num = frames.shape[0]
    result_mat = np.zeros(frames.shape[1:])
    for i in range(frame_num):
        fr = frames[i]
        result_mat += fr
    return result_mat


def slidesViewFrames(frames):
    '''
    Show all frames in a mrc file
    '''
    frame_num = frames.shape[0]
    result_mat = np.zeros(frames.shape[1:])
    for i in range(frame_num):
        fr = frames[i]
        demoArrDataCV(fr)


def writeMrcFile(data, mrcfh):
    pass


def writeH5dataset(data, h5fh):
    pass


def main():
    frame_data = readArrayMrc(frame_path)[0]
    # frame_data = (frame_data - frame_data.min()) / \
    #     (frame_data.max() - frame_data.min()) * 255
    norm_data = readArrayMrc(norm_path)
    # norm_data = (norm_data - norm_data.min()) / \
    #     (norm_data.max() - norm_data.min()) * 255

    print(frame_data.shape)
    print(norm_data.shape)
    # demoArrayData(frame_data, args='Frame.png')
    # demoArrayData(norm_data, args='Norm.png')
    # demoArrayData(frame_data, norm_data)

    # demoArrDataCV(frame_data, args='Frame.jpg')
    # demoArrDataCV(norm_data, args='Norm.jpg')
    # demoArrDataCV(np.multiply(frame_data, norm_data), args='Sample.jpg')
    frames_data = readArrayMrc(frame_path)
    result_mat = overlayFramesNorm(frames_data, norm_data)
    demoArrDataCV(result_mat, args='Overlay.jpg')
    # slidesViewFrames(frames_data)


if __name__ == '__main__':
    main()
