import signalProcessor
import numpy as np
class LimitSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, mi=None, ma=None):
        signalProcessor.SignalProcessor.__init__(self, "clip")
        self.mi = mi
        self.ma = ma


    def processSimple(self, signalIn):
        return np.clip(signalIn,self.mi,self.ma)

