import signalProcessor
import numpy as np
class DbSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, scale=1.0, ref = 1.0, factor = 20.0):
        signalProcessor.SignalProcessor.__init__(self, "dB")
        self.scale = scale
        self.factor = factor
        self.ref = ref

    def process(self, signalIn):
        return self.factor*np.log10(np.abs(signalIn)/self.ref)

