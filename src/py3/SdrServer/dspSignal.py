import time

class Signal:
    def __init__(self, samples=None, domain=None, fc=None, rate=None, shift = None, baseSig =None):
        self.t0 = time.time()
        if baseSig is not None:
            self.t0 = baseSig.t0
            self.samples = baseSig.samples
            self.domain = baseSig.domain
            self.fc = baseSig.fc
            self.rate = baseSig.rate
            self.shift = baseSig.shift
        if samples is not None:
            self.samples = samples
        if domain is not None:
            self.domain = domain
        if fc is not None: 
            self.fc = fc
        if rate is not None:
            self.rate = rate
        if shift is not None:
            self.shift = shift

