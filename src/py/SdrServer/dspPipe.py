import threading
import Queue
import prctl
import time

class DspPipe(threading.Thread):
    def __init__(self, proc = [], out = []):
        threading.Thread.__init__(self)
        self.q = Queue.Queue()
        self.out = out
        self.processors = proc
        self.desc = ''
        for p in self.processors:
            self.desc+=p.name+' '
        self.d = 0
        self.tot = 0
        self.done = False

    
    def putSamples(self, samples):
        if samples is not None:
            self.tot+=1
            if self.q.qsize() < 800:
                self.q.put(samples)
            else:
                self.d+=1
                print self.desc, "dropping input. Total inputs dropped", self.d, "of", self.tot

    def run(self):

        print self.desc, "is runing"
        prctl.set_name("DSP pipe "+self.desc)
        while True:
            if self.done:
                break
            try:
                if not self.processors[0].source:
                    si = self.q.get(timeout=0.01);
                else:
                    si = None

                for p in self.processors:
                    so = p.process(si)
                    si = so
                for o in self.out:
                    o.putSamples(so)
                so = None
                si = None
            except Queue.Empty:
                if self.done:
                    break
        print self.desc, "is done, stopping"
        for p in self.processors:
            so = p.stop()

    def stop(self):
        self.done = True


