import signalProcessor
import dspSignal
import numpy as np
class FmMod(signalProcessor.SignalProcessor):
    def __init__(self, sensitivity):
        self.s = sensitivity #Hz per unit
        signalProcessor.SignalProcessor.__init__(self, "fmmod")
        self.tlast = 0.0

    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig=signalIn)
        t = np.arange(len(signalIn.samples))/signalIn.rate+1.0/signalIn.rate+self.tlast
        signalOut.samples = np.exp(1.0j*np.pi*2.0*signalIn.samples*t)
        self.tlast = t[-1]
        return signalOut

