import signalProcessor
import dspSignal
#import kivyPlot as plot
#import glfwplot as plot
import glutplot as plot
import numpy as np
import time
class FftPlot(signalProcessor.SignalProcessor):
    def __init__(self, title = "Plot", nmax=None):
        signalProcessor.SignalProcessor.__init__(self, "fftplot")
        self.fig = plot.Figure(title)
        self.nmax=nmax

    def stop(self):
        self.fig.close()

    def process(self, signalIn):
        signalOut = signalIn

        if not self.fig.isReady():
            return signalOut

        if self.nmax is None:
            nsamp = len(signalIn.samples)
        else:
            nsamp = min(len(signalIn.samples), self.nmax)

        signalOut = dspSignal.Signal(baseSig = signalIn)
        ft = np.fft.fftshift(np.fft.fft(signalIn.samples[0:nsamp]))
        db = np.clip(20*np.log10(np.abs(ft)), -100, None)
        fax = np.linspace(-signalIn.rate, signalIn.rate, nsamp)-signalIn.shift
        self.fig.plot(fax, db)
        return signalOut

