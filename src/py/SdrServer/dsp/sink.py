import signalProcessor
import numpy as np
import scipy.signal
import time
class Sink(signalProcessor.SignalProcessor):
    def __init__(self, dev, name = "sink"):
        signalProcessor.SignalProcessor.__init__(self, name)
        self.dev = dev

    def processSimple(self, signalIn):
        self.dev.putSamples(np.vstack((signalIn,signalIn)).T)
        return signalIn

