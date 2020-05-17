import numpy as np
import threading
import sounddevice as sd
import time
import matplotlib.pyplot as plt
#import kivyPlot

class SoundDevice(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.lock.acquire()
        self.il = threading.Lock()
        self.ol = threading.Lock()
        self.maxObuf = 32768
        self.maxIbuf = 32768
        self.ibuf = []
        self.obuf = []
        self.start()

    def callback(self, indata, outdata, frames, time, status):
        if status:
            if self.ibuf != []:
                print("ibuf", self.ibuf.shape, end=' ')
            if self.obuf != []:
                print("obuf", self.obuf.shape, end=' ')

            print(status)
        #outdata[:] = indata
        self.ol.acquire()
        if len(self.obuf) > 0:
            if len(outdata) < len(self.obuf):
                ns = len(outdata)
            else:
                ns = len(self.obuf)
            outdata[0:ns] = self.obuf[0:ns]
            self.obuf = self.obuf[ns:]
            if ns < len(outdata):
                outdata[ns:] = indata[ns:]*0
        else:
            #print "Obuf empty", len(indata), indata.shape
            outdata[:] = indata*0

        self.ol.release()

        self.il.acquire()
        if len(self.ibuf) < self.maxIbuf:
            if self.ibuf == []:
                self.ibuf = indata
            else:
                self.ibuf = np.concatenate((self.ibuf, indata))
        self.il.release()


    def run(self):
        stream = sd.Stream(channels=2, callback=self.callback, latency=0.025)
        print("latency", stream.latency)
        with stream:
            print(dir(stream))
            self.lock.acquire()

    def getSamplesInternal(self, n=None):
        self.il.acquire()
        if n is not None:
            if n > len(self.ibuf):
                self.il.release()
                return np.array([])
            dr = self.ibuf[0:n]
            self.ibuf = self.ibuf[n:]
            self.il.release()
            return dr[:,0]
        else:
            dr = self.ibuf
            self.ibuf = []
            self.il.release()
            return dr[:,0];

    def getSamples(self, n):
        while True:
            s = self.getSamplesInternal(n)
            if len(s) == 0:
                time.sleep(0.0001)
            else:
                return s

    def putSamples(self, samples):
        self.ol.acquire()
        #if len(self.obuf) < self.maxObuf:
        if self.obuf == []: 
            self.obuf = samples 
        else:
            self.obuf = np.concatenate((self.obuf, samples))
        self.ol.release()


    def stop(self):
        self.lock.release();


sd.default.samplerate = 44000
sd.default.channels = 1
