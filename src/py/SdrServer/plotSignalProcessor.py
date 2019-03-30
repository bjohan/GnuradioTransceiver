import signalProcessor
import kivyPlot
import numpy as np
import time
class PlotSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self):
        signalProcessor.SignalProcessor.__init__(self, "Plot")
        self.fig = kivyPlot.Figure()

    def stop(self):
        self.fig.stop()

    def process(self, signalIn):
        self.fig.plot(signalIn)
        return signalIn

