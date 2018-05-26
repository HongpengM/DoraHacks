import collections


class para(object):
    """doc string for param"""
    crop_offsetx = None
    crop_offsety = None
    crop_nsam = None

    nBin = None

    nStart = None
    # first frame(0 - base)
    nEnd = None
    # last frame(0 - base)
    nStartSum = None
    # first frame to sum(0 - base)
    nEndSum = None
    # last frame to sum(0 - base)

    GPUNum = None
    # GPU device ID

    bfactor = None
    # in pix ^ 2
    CCPeakSearchDim = None
    # search peak in this box
    FrameDistOffset = None
    NoisePeakSize = None
    kiThresh = None
    # alignment error threshold in pixel
    bHGain = None
    bGain = None
    bDark = None

    bSaveRawSum = None
    bSaveStackRaw = None
    bSaveStackCorr = None
    bSaveCCmap = None
    bSaveLog = None

    bAlignToMid = None

    # display para
    fftscale = None
    bDispSumCorr = None
    bDispFFTRaw = None
    bDispFFTCorr = None
    bDispCCMap = None
    bDispFSC = None
    bLogFSC = None

    # reserved parameters for Dialog window
    fscMax = None

    #  ------------------------------------
    __dict__ = {}

    def __init__(self):
        super(para, self).__init__()
        self.setDefaultPara()

    def tryIndexItemInList(li, item):
        idx = None
        try:
            li.index(item)
        except ValueError:
            idx = None
        return idx

    def getPara(self, argc):
        if type(argc) == type({}):
            for k, v in argc.items():
                if k in self.__dict__.keys():
                    self.__dict__[k] = v
        else type(argc) == type([]):
            if len(argc) % 2 != 0:
                return False
            else:
                idx = tryIndexItemInList(argc, '-crx')
                if idx:
                    self.crop_offsetx = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-cry')
                if idx:
                    self.crop_offsety = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-cdx')
                if idx:
                    self.crop_nsam[0] = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-cdy')
                if idx:
                    self.crop_nsam[1] = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-bin')
                if idx:
                    self.nBin = int(argc[idx + 1])
                    if self.nBin > 2:
                        print('Larger than maximum binning 2. Set to 2.\n')
                        self.nBin = 2

                idx = tryIndexItemInList(argc, '-nst')
                if idx:
                    self.nStart = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-ned')
                if idx:
                    self.nEnd = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-nss')
                if idx:
                    self.nStartSum = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-nes')
                if idx:
                    self.nEndSum = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-gpu')
                if idx:
                    self.GPUNum = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-bft')
                if idx:
                    self.bfactor = float(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-pbx')
                if idx:
                    self.CCPeakSearchDim = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-fod')
                if idx:
                    self.FrameDistOffset = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-nps')
                if idx:
                    self.NoisePeakSize = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-kit')
                if idx:
                    self.kiThresh = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-hgr')
                if idx:
                    self.bHGain = int(argc[idx + 1])

                # FGR has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-fgr')
                if idx:
                    self.bGain = int(argc[idx + 1])
                # FDR has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-fdr')
                if idx:
                    self.FrameDistOffset = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-srs')
                if idx:
                    self.bSaveRawSum = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-ssr')
                if idx:
                    self.bSaveStackRaw = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-ssc')
                if idx:
                    self.bSaveStackCorr = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-scc')
                if idx:
                    self.bSaveCCmap = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-slg')
                if idx:
                    self.bSaveLog = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-atm')
                if idx:
                    self.bAlignToMid = int(argc[idx + 1])

                # DISP has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-dsp')
                if idx:
                    self.bSaveRawSum = int(argc[idx + 1])

                idx = tryIndexItemInList(argc, '-fsc')
                if idx:
                    self.bLogFSC = int(argc[idx + 1])

                # FRS has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-frs')
                if idx:
                    self.bSaveStackCorr = int(argc[idx + 1])
                # FCS has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-fcs')
                if idx:
                    self.bSaveStackCorr = int(argc[idx + 1])
                # FRT has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-frt')
                if idx:
                    self.bSaveCCmap = int(argc[idx + 1])
                # FCT has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-fct')
                if idx:
                    self.bSaveLog = int(argc[idx + 1])
                # FCM has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-fcm')
                if idx:
                    self.bAlignToMid = int(argc[idx + 1])
                # FLG has some modifications to made to be consistent with
                # original code
                idx = tryIndexItemInList(argc, '-flg')
                if idx:
                    self.bAlignToMid = int(argc[idx + 1])
        else:
            print('Undefined arg type')

        # Set File Name
        return True

    def dictPara(self):
        paradict = {}
        paradict['crop_offsetx'] = self.crop_offsetx
        paradict['crop_offsety'] = self.crop_offsety
        paradict['crop_nsam'] = self.crop_nsam

        paradict['nBin'] = self.nBin

        paradict['nStart'] = self.nStart
        # first frame(0 - base)
        paradict['nEnd'] = self.nEnd
        # last frame(0 - base)
        paradict['nStartSum'] = self.nStartSum
        # first frame to sum(0 - base)
        paradict['nEndSum'] = self.nEndSum
        # last frame to sum(0 - base)

        paradict['GPUNum'] = self.GPUNum
        # GPU device ID

        paradict['bfactor'] = self.bfactor
        # in pix ^ 2
        paradict['CCPeakSearchDim'] = self.CCPeakSearchDim
        # search peak in this box
        paradict['FrameDistOffset'] = self.FrameDistOffset
        paradict['NoisePeakSize'] = self.NoisePeakSize
        paradict['kiThresh'] = self.kiThresh
        # alignment error threshold in pixel
        paradict['bHGain'] = self.bHGain
        paradict['bGain'] = self.bGain
        paradict['bDark'] = self.bDark

        paradict['bSaveRawSum'] = self.bSaveRawSum
        paradict['bSaveStackRaw'] = self.bSaveStackRaw
        paradict['bSaveStackCorr'] = self.bSaveStackCorr
        paradict['bSaveCCmap'] = self.bSaveCCmap
        paradict['bSaveLog'] = self.bSaveLog

        paradict['bAlignToMid'] = self.bAlignToMid

        # display para
        paradict['fftscale'] = self.fftscale
        paradict['bDispSumCorr'] = self.bDispSumCorr
        paradict['bDispFFTRaw'] = self.bDispFFTRaw
        paradict['bDispFFTCorr'] = self.bDispFFTCorr
        paradict['bDispCCMap'] = self.bDispCCMap
        paradict['bDispFSC'] = self.bDispFSC
        paradict['bLogFSC'] = self.bLogFSC

        # reserved parameters for Dialog window
        paradict['fscMax'] = self.fscMax
        self.__dict__ = paradict

    def displayPara(self):
        if not self.__dict__:
            self.__dict__ = {}
        if len(self.__dict__) == 0:
            self.dictPara()
        od = collections.OrderedDict(sorted(self.__dict__.items()))
        print('>' * 15, 'Parameters', '<' * 15)
        for k, v in od.items():
            print(k, ': ', v)
        print('>' * 15, 'Parameters End', '<' * 15)

    def setDefaultPara(self):
        self.crop_offsetx = 0
        self.crop_offsety = 0
        self.crop_nsam = [0, 0]

        self.nBin = 1

        self.nStart = 0
        # first frame(0 - base)
        self.nEnd = 0
        # last frame(0 - base)
        self.nStartSum = 0
        # first frame to sum(0 - base)
        self.nEndSum = 0
        # last frame to sum(0 - base)

        self.GPUNum = 0
        # GPU device ID

        self.bfactor = 150
        # in pix ^ 2
        self.CCPeakSearchDim = 96
        # search peak in this box
        self.FrameDistOffset = 2
        self.NoisePeakSize = 0
        self.kiThresh = 1.0
        # alignment error threshold in pixel
        self.bHGain = True
        self.bGain = False
        self.bDark = False

        self.bSaveRawSum = False
        self.bSaveStackRaw = False
        self.bSaveStackCorr = False
        self.bSaveCCmap = False
        self.bSaveLog = True

        self.bAlignToMid = 1

        # display para
        self.fftscale = 0.0001
        self.bDispSumCorr = True
        self.bDispFFTRaw = True
        self.bDispFFTCorr = True
        self.bDispCCMap = True
        self.bDispFSC = False
        self.bLogFSC = False

        # reserved parameters for Dialog window
        self.fscMax = 0.25


if __name__ == '__main__':
    testPara = para()
    testPara.setDefaultPara()
    print(len(testPara.__dict__))
    print(testPara.displayPara())
