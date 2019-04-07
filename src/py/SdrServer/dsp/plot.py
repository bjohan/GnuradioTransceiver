import signalProcessor
#import kivyPlot as plot
#import glfwplot as plot
import glutplot as plot
import numpy as np
import dspSignal
import time
class Plot(signalProcessor.SignalProcessor):
    def __init__(self, title = plot):
        signalProcessor.SignalProcessor.__init__(self, "plot")
        self.fig = plot.Figure(title)

    def stop(self):
        self.fig.close()

    def process(self, signalIn):
        signalOut = signalIn
        if not self.fig.isReady():
            return signalOut
        #signalOut = dspSignal.Signal(baseSig = signalIn)
        x = np.arange(len(signalIn.samples))/float(signalIn.rate)
        self.fig.plot(x, np.real(signalIn.samples))
        return signalOut

