class SignalProcessor:
    def __init__(self, name, source = False):
        self.source = source
        self.name = name

    def stop(self):
        pass

    def process(self, signalIn):
        return signalIn
