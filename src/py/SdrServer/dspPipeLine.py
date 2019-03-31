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
            

    def status(self):
        lt = 0
        for p in self.pipes:
            if p.computed >0:
                rate = (p.computeTime/p.computed) 
            else:
                rate = 0
            num = p.q.qsize()
            print p.desc, num, "%.2e"%(rate), 
            lt+=rate*(num+1)
        print "lat %.2fms"%(lt*1000)
