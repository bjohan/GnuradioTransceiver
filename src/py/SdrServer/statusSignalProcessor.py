import signalProcessor
import time
class StatusSignalProcessor(signalProcessor.SignalProcessor):
    def __init__(self, rate = 1.0):
        signalProcessor.SignalProcessor.__init__(self, "Status")
        self.rate = rate
        self.nt = time.time()
        self.frames = 0
        self.samples = 0
        self.lt = time.time()

    def process(self, signalIn):
        self.frames+=1
        self.samples+=len(signalIn.samples)
        if time.time() > self.nt:
            elapsed = time.time()-self.lt
            print "latency", time.time()-signalIn.t0, "fps", float(self.frames)/elapsed, "sps", float(self.samples)/elapsed
            self.samples = 0
            self.frames = 0
            self.nt = time.time()+self.rate;
            self.lt = time.time()
        return signalIn

