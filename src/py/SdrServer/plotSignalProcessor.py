import signalProcessor
#import kivyPlot as plot
import glfwplot as plot
import numpy as np
import time
class PlotSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self):
        signalProcessor.SignalProcessor.__init__(self, "Plot")
        self.fig = plot.Figure()

    def stop(self):
        self.fig.close()

    def process(self, signalIn):
        self.fig.plot(np.arange(len(signalIn)), signalIn)
        return signalIn

