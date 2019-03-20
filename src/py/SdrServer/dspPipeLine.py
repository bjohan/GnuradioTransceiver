import dspPipe
class DspPipeLine:
    def __init__(self, pipeline):
        self.pipes=[]
        lp = []
        for p in reversed(pipeline):
            self.pipes.insert(0, dspPipe.DspPipe(proc=p, out = lp))
            lp = [self.pipes[0]]

    def start(self):
        for p in reversed(self.pipes):
            p.start()

    def stop(self):
        for p in self.pipes:
            p.stop()
            

