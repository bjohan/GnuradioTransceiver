import threading

class SourceSinkHalfDuplex:
    def __init__(self, sourceSink):
        self.sourceSink = sourceSink
        self.lock = threading.Lock()
        self.gotLock = False

    def getSamples(self, n):
        with self.lock:
            return self.sourceSink.getSamples(n)

    def putSamples(self, samples):
        if samples is not None:
            if not self.gotLock:
                self.lock.acquire()
                self.gotLock = True
            self.sourceSink.putSamples(samples)
        else:
            self.lock.release()
            self.gotLock = False

