import signalProcessor
import numpy as np
import scipy.signal
import time
class Sink(signalProcessor.SignalProcessor):
    def __init__(self, sndDev):
        signalProcessor.SignalProcessor.__init__(self, "audio")
        self.dev = sndDev

    def processSimple(self, signalIn):
        self.dev.putSamples(np.vstack((signalIn,signalIn)).T)
        return signalIn

