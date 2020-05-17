from . import signalProcessor
import numpy as np
import dspSignal
class Printer(signalProcessor.SignalProcessor):
    def __init__(self):
        signalProcessor.SignalProcessor.__init__(self, "print")

    def stop(self):
        pass

    def process(self, signalIn):
        signalOut = signalIn
        print(signalIn.samples.shape)
        print(signalIn.samples)
        return signalOut

