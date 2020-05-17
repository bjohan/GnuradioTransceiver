import dspSignal
class SignalProcessor:
    def __init__(self, name, source = False):
        self.source = source
        self.name = name

    def stop(self):
        pass

    def processSimple(self, samples):
        return samples

    def process(self, signalIn):
        signalOut = dspSignal.Signal(baseSig = signalIn);
        signalOut.samples = self.processSimple(signalIn.samples)
        return signalOut
