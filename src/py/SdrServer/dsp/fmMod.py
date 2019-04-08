import signalProcessor
import dspSignal
import numpy as np
class FmMod(signalProcessor.SignalProcessor):
    def __init__(self, sensitivity):
        self.s = float(sensitivity) #Hz per unit
        signalProcessor.SignalProcessor.__init__(self, "fmmod")
        self.plast = 0.0

    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig=signalIn)
        #t = np.arange(len(signalIn.samples))/float(signalIn.rate)+1.0/signalIn.rate+self.tlast #time 
        rate = np.cumsum(np.real(signalIn.samples*self.s))/float(signalIn.rate)
        cp = np.pi*2*rate+self.plast
        #print cp
        #signalOut.samples = signalIn.samples*np.exp(-1.0j*np.pi*2.0*t)
        signalOut.samples =  np.exp(1.0j*cp)
        self.plast = cp[-1]%np.pi
        return signalOut

