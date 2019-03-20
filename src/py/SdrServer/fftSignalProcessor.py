import signalProcessor
import numpy as np
class FftSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, samples=1024):
        signalProcessor.SignalProcessor.__init__(self, "FFT")
        self.samples = samples

    def process(self, signalIn):
        n = min(len(signalIn), self.samples)
        s = signalIn[0:n]
        return np.fft.fftshift(np.fft.fft(s-np.mean(s)))

