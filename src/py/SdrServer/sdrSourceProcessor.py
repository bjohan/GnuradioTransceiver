import signalProcessor
import numpy as np
import scipy.signal
import time
class SdrSourceProcessor(signalProcessor.SignalProcessor):
    def __init__(self, sdr, samples = 8192):
        signalProcessor.SignalProcessor.__init__(self, "SDR", source=True)
        self.sdr = sdr
        self.samples = samples
        self.tlast = time.time()
        

    def process(self, signalIn):
        #time.sleep(0.001)
        #tIdle = time.time()-self.tlast
        #t0 = time.time()
        samples = self.sdr.getRxSamples(self.samples)
        #tRead = time.time()-t0
        #self.tlast = time.time()
        #if samples is None: 
        #    print "No samples got during read... Idle", tIdle, "read", tRead, "Duty", (tRead/(tIdle+tRead))
        return samples

