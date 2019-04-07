import dspSignal
import signalProcessor
import numpy as np
import scipy
class ResamplingSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, outputRate):
        signalProcessor.SignalProcessor.__init__(self, "resampling")
        self.outputRate =  float(outputRate)
        self.rest = []
        self.lastIn = None

    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig=signalIn)
        #TODO, must be updated so that samples betwen vector chunks are also interpolated

        #Setup data to be resampled, if there is an old sample, add to beginning of vector
        if self.lastIn is None:
            interpSamples =signalIn.samples
        else:
            interpSamples = np.hstack((np.array([self.lastIn]), signalIn.samples))
        timeAxis = np.arange(len(interpSamples))/float(signalOut.rate)

        self.lastIn = None #signalIn.samples[-1]

        rsr = self.outputRate/float(signalIn.rate)
        numOutSamp =  np.floor(len(timeAxis)*rsr)
        resampTime = np.arange(numOutSamp-rsr)/self.outputRate
        interpolator = scipy.interpolate.interp1d(timeAxis, interpSamples, assume_sorted = False)
        #print "ta", timeAxis
        #print "sa", interpSamples
        #print "rt", resampTime
        #print "rsr", rsr

        signalOut.samples = interpolator(resampTime)
        signalOut.rate = self.outputRate

        return signalOut 

