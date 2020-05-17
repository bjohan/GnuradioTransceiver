from . import signalProcessor
import dspSignal
import numpy as np
class Tuner(signalProcessor.SignalProcessor):
    def __init__(self, nco=0.0):
        signalProcessor.SignalProcessor.__init__(self, "tune")
        self.nco = float(nco)
        self.ph = 0.0


    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig=signalIn)
        phaseRate = 2.0*np.pi*self.nco/signalIn.rate
        phases = (self.ph+np.arange(len(signalIn.samples))*phaseRate)
        self.ph = phases[-1]+phaseRate
        signalOut.shift += self.nco
        signalOut.samples = signalIn.samples*np.exp(1j*phases)
        return signalOut

