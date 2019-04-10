import signalProcessor
import dspSignal
import numpy as np
class AcCouple(signalProcessor.SignalProcessor):
    def __init__(self):
        signalProcessor.SignalProcessor.__init__(self, "ac")


    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig=signalIn)
        signalOut.samples = signalIn.samples-np.mean(signalIn.samples)
        return signalOut

