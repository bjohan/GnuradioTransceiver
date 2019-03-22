import signalProcessor
import numpy as np
import scipy.signal
import time
class SoundSinkProcessor(signalProcessor.SignalProcessor):
    def __init__(self, sndDev):
        signalProcessor.SignalProcessor.__init__(self, "audio")
        self.dev = sndDev
        

    def process(self, signalIn):
        #print signalIn
        self.dev.putSamples(np.vstack((signalIn,signalIn)).T)
        return signalIn
