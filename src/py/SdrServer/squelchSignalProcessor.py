import signalProcessor
import dspSignal
import numpy as np
class SquelchSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, threshold=200, delay=0.5):
        signalProcessor.SignalProcessor.__init__(self, "squelch")
        self.overrange = 0


    def processSimple(self, signalIn):
        signalOut = dspSignal.Signal(baseSig=signalIn)
        
        sabs = np.abs(signalIn)
        for i in range(len(signalIn)):
            newabs = sabs[i]*self.g
            if newabs < self.target:
                self.g*=(1.0+self.rate)
            else: 
                if newabs > self.maxAmp:
                    self.overrange+=1
                    if self.overrange >= self.overrangeNum:
                        self.g = self.target/newabs
                else:
                    self.overrange = 0
                    self.g*=(1.0-self.rate)
            signalIn[i] *= self.g
            
        return signalIn

