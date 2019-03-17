import numpy as np
import threading
import sounddevice as sd
import time
import matplotlib.pyplot as plt
import kivyPlot

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
                print "ibuf", self.ibuf.shape,
            if self.obuf != []:
                print "obuf", self.obuf.shape,

            print status
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
                outdata[ns:] = outdata[ns:]*0
        self.ol.release()

        self.il.acquire()
        if len(self.ibuf) < self.maxIbuf:
            if self.ibuf == []:
                self.ibuf = indata
            else:
                self.ibuf = np.concatenate((self.ibuf, indata))
        self.il.release()


    def run(self):
        with(sd.Stream(channels=2, callback=self.callback)):
            self.lock.acquire()

    def getSamples(self, n=None):
        self.il.acquire()
        if n is not None:
            if n > len(self.ibuf):
                self.il.release()
                return []
            dr = self.ibuf[0:n]
            self.ibuf = self.ibuf[n:]
            self.il.release()
            return dr
        else:
            dr = self.ibuf
            self.ibuf = []
            self.il.release()
            return dr;

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
sd.default.channels = 2
print "Creating sound device"
d  = SoundDevice()
cs = 0;
def generateSamples():
    global d
    global cs
    while True:
        tv = np.linspace(cs,cs+8191,8192);
        yv = np.sin(tv/10.0)*0.1
        d.putSamples(np.vstack((yv, yv)).T)
        cs += 8192
        time.sleep(0.1)

#thr = threading.Thread(target=generateSamples)
#thr.start()
try:
    while True:
        #plt.hold(False)
        s = d.getSamples(1024)
        if s != []:
            #print "plot", s
            kivyPlot.plot(s)
            #plt.plot(s)
            #plt.draw()
            #plt.pause(0.000001)
        else:
            time.sleep(0.001)
except KeyboardInterrupt:
    print "Control-C pressed, shuting down"


#print "Waiting for thread to join"
#time.sleep(3)
kivyPlot.stop()
d.stop()
d.join()
#print "Done"
kivyPlot.join()
