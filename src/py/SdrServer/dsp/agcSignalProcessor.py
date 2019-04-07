import signalProcessor
import numpy as np
class AgcSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, rate = 0.01, target = 1.0, maxAmp = 2.0, overrangeNum = 10):
        signalProcessor.SignalProcessor.__init__(self, "agc")
        self.rate = rate
        self.target = target
        self.maxAmp = maxAmp
        self.g = 1.0
        self.overrangeNum = overrangeNum
        self.overrange = 0


    def processSimple(self, signalIn):
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

