import signalProcessor
import numpy as np
class DecimationSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, factor=10):
        signalProcessor.SignalProcessor.__init__(self, "decimation")
        self.factor = int(factor)
        self.rest = []

    def process(self, signalIn):
        allsample = np.hstack( (self.rest, signalIn))
        outSample=np.floor(len(allsample)/self.factor)
        last = int(outSample*self.factor)
        signalOut=allsample[0:last:self.factor]
        self.rest = allsample[last:]
        return signalOut 
