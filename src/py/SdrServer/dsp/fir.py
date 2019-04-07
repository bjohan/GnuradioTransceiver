import signalProcessor
import numpy as np
import scipy.signal
class Fir(signalProcessor.SignalProcessor):
    def __init__(self, taps = 32, passBand = 0.5, transition = 0.1):
        signalProcessor.SignalProcessor.__init__(self, "FIR")
        self.taps  = scipy.signal.firwin(taps, passBand,width=transition, pass_zero=True)

    def processSimple(self, signalIn):
        #return scipy.signal.convolve(signalIn, self.taps, mode='valid')
        return np.convolve(signalIn, self.taps, mode='valid')

