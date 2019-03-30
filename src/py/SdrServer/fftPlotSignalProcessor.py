import signalProcessor
import dspSignal
#import kivyPlot as plot
import glfwplot as plot
import numpy as np
import time
class FftPlotSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, title = "Plot"):
        signalProcessor.SignalProcessor.__init__(self, "fftplot")
        self.fig = plot.Figure(title)

    def stop(self):
        self.fig.close()

    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig = signalIn)
        ft = np.fft.fftshift(np.fft.fft(signalIn.samples))
        db = np.clip(20*np.log10(np.abs(ft)), -100, None)
        fax = np.linspace(-signalIn.rate, signalIn.rate, len(signalIn.samples))
        self.fig.plot(fax, db)
        return signalOut

