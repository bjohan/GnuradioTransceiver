import numpy as np
import scipy.interpolate
import time

class HeightResampler:
    def __init__(self, source):
        self.src = source

    def getContained(self, vb, vs):
        #get elements in vb which are bounded by smallest and largest element in vs
        mi = np.min(vs)
        ma = np.max(vs)
        #print "min", mi, "max", ma
        #print "vb", vb
        return np.where(np.logical_and(vb >= mi, vb <= ma))

    def nearIdx(self, full, sparse):
        v = []
        for s in sparse:
            v.append((np.abs(full-s)).argmin())
        return np.array([v])


    def resample(self, xs, ys, vs, xn, yn):
        sx = self.nearIdx(xs, xn)
        sy = self.nearIdx(ys, yn).T
        #print "sx", sx.shape, "sy", sy.shape
        return vs[sy, sx].T

    def get(self, xs, ys):
        result = np.zeros((len(ys), len(xs)))
        yi=0
        while yi < len(ys):
            xi=0
            while xi < len(xs):
                #print
                xinc = 1
                yinc = 1
                tread = time.time()
                e, xr, yr = self.src.getBlock(xs[xi],ys[yi])
                tread = time.time()-tread
                #print "xr", xr
                #print "yr", yr
                tprep = time.time()
                xtg = self.getContained(xs, xr)
                ytg = self.getContained(ys, yr)
                tprep = time.time()-tprep
                #print "xtg", xtg[0]
                #print "ytg", ytg[0]
                #interpFunc = scipy.interpolate.interp2d(xr, yr, e)
                tint = time.time()
                rsd = self.resample(xr, yr, e, xs[xtg[0]], ys[ytg[0]])
                #print "Resampled shape", rsd.shape
                result[-ytg[0],np.array([xtg[0]]).T] = rsd
                #for yvi in ytg[0]:
                #    for xvi in xtg[0]:
                #        #print "xvi", xvi, "yvi", yvi
                #        result[-yvi, xvi]=interpFunc(xs[xvi], ys[yvi])
                #        pass
                tint = time.time()-tint
                print("read", tread, "prepare", tprep, "interpolate", tint, yi/float(len(ys)))
                xinc = len(xtg[0])
                yinc = len(ytg[0])
                xi+=xinc
            yi+=yinc
        return result




