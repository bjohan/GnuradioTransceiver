import signalProcessor
import dspSignal
import numpy as np
class FmDemod(signalProcessor.SignalProcessor):
    def __init__(self):
        signalProcessor.SignalProcessor.__init__(self, "fmdemod")

    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig=signalIn)
        ph = np.diff(np.unwrap(np.angle(signalIn.samples)))
        signalOut.samples = ph
        return signalOut

