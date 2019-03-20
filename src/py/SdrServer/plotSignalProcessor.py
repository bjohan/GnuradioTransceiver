import signalProcessor
import kivyPlot
import numpy as np
import time
class PlotSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self):
        signalProcessor.SignalProcessor.__init__(self, "Plot")
        self.fig = kivyPlot.Figure()
        #self.tlast = time.time()

    def stop(self):
        self.fig.stop()

    def process(self, signalIn):
        #tIdle = time.time()-self.tlast
        #tActive = time.time()
        self.fig.plot(signalIn)
        #tActive = time.time()-tActive
        #print "Active", tActive, "idle", tIdle
        #self.tlast = time.time()
        return signalIn

