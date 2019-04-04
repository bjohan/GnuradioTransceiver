import signalProcessor
import numpy as np
import time
import dspSignal
class SoundSourceProcessor(signalProcessor.SignalProcessor):
    def __init__(self, sndDev, samples = 8192):
        signalProcessor.SignalProcessor.__init__(self, "sndsrc", source=True)
        self.sndDev = sndDev
        self.samples = samples
        

    def process(self, signalIn):
        samples = []
        while samples == []:
            samples = self.sndDev.getSamples(self.samples)
            time.sleep(0.001)
        #print samples
        #print "samples shape", samples.shape
        samples = samples[:,1]
        return dspSignal.Signal(samples=samples, domain='time', fc=0, rate = 44000, shift = 0)

