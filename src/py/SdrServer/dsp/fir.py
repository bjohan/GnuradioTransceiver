import signalProcessor
import numpy as np
import scipy.signal
class Fir(signalProcessor.SignalProcessor):
    def __init__(self, taps = 32, passBand = 0.5, transition = 0.1):
        signalProcessor.SignalProcessor.__init__(self, "FIR")
        self.taps  = scipy.signal.firwin(taps, passBand,width=transition, pass_zero=True)
        self.ntaps = taps
        self.last = []

    def processSimple(self, signalIn):
        #return scipy.signal.convolve(signalIn, self.taps, mode='valid')
        toFilt = np.hstack((self.last, signalIn))
        self.last = signalIn[-self.ntaps:]
        return np.convolve(toFilt, self.taps, mode='valid')

