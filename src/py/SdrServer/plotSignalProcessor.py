import signalProcessor
#import kivyPlot as plot
import glfwplot as plot
import numpy as np
import dspSignal
import time
class PlotSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, title = plot):
        signalProcessor.SignalProcessor.__init__(self, "plot")
        self.fig = plot.Figure(title)

    def stop(self):
        self.fig.close()

    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig = signalIn)
        x = np.arange(len(signalIn.samples))/signalIn.rate
        self.fig.plot(x, signalIn.samples)
        return signalOut

