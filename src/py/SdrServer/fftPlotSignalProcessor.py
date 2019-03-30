import signalProcessor
#import kivyPlot as plot
import glfwplot as plot
import numpy as np
import time
class FftPlotSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self):
        signalProcessor.SignalProcessor.__init__(self, "Plot")
        self.fig = plot.Figure()

    def stop(self):
        self.fig.close()

    def process(self, signalIn):
        ft = np.fft.fftshift(np.fft.fft(signalIn))
        db = np.clip(20*np.log10(np.abs(ft)), -100, None)
        self.fig.plot(np.arange(len(db)), db)
        return signalIn

