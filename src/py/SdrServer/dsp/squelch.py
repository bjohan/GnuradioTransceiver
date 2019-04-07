import signalProcessor
import dspSignal
import numpy as np
class Squelch(signalProcessor.SignalProcessor):
    def __init__(self, threshold=200, hold=0.5):
        signalProcessor.SignalProcessor.__init__(self, "squelch")
        self.threshold = threshold
        self.hold = hold
        self.t = hold



    def process(self, signalIn):
        signalOut = None
        if max(np.abs(signalIn.samples)) > self.threshold:
            self.t = 0.0;
            signalOut = signalIn
        if self.t < self.hold:
            signalOut = signalIn

        self.t += float(len(signalIn.samples))/float(signalIn.rate)
        return signalOut

