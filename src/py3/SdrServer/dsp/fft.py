import signal
from . import signalProcessor
import numpy as np
class Fft(signalProcessor.SignalProcessor):
    def __init__(self, samples=1024):
        signalProcessor.SignalProcessor.__init__(self, "FFT")
        self.samples = samples

    def process(self, signalIn):
        signalOut = signal.Signal(baseSig=signalIn)
        n = min(len(signalIn.samples), self.samples)
        s = signalIn.samples[0:n]
        signalOut.samples=np.fft.fftshift(np.fft.fft(s-np.mean(s)))
        signalOut.domain='frequency'
        return signalOut

