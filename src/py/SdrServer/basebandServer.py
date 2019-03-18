import matplotlib.pyplot as plt
import kivyPlot
import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy as np#use numpy for buffers
from sdrDevice import SdrDeviceBase


class SdrDevice(SdrDeviceBase):
    #Class that will service each baseband device
    def __init__(self, bbdev):
        self.bbdev = bbdev
        self.sdr = SoapySDR.Device(bbdev)
        self.rxStreamActiveState = False;
        self.txStreamActiveState = False;
        self.rxStream = None
        self.txStream = None
        #print dir(self.sdr)
        #print help(self.sdr.setGainMode)
        self.sdr.setGainMode(SOAPY_SDR_RX,0,False)
        self.sdr.setGain(SOAPY_SDR_RX, 0, 0+0*100)
    
    def listAntennas(self):
        return {'rx': self.sdr.listAntennas(SOAPY_SDR_RX, 0),
            'tx': self.sdr.listAntennas(SOAPY_SDR_TX, 0)}
    

    def listGains(self):
        return {'rx': self.sdr.listGains(SOAPY_SDR_RX, 0),
            'tx': self.sdr.listGains(SOAPY_SDR_TX, 0)}
        
    def listFreqs(self):
        rxfs = []
        txfs = []
        rl = self.sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
        for r in rl:
            #print "R is", dir(r)
            #print "minimum", r.minimum()
            rxfs.append((r.minimum(), r.maximum(), r.step()))
        tl = self.sdr.getFrequencyRange(SOAPY_SDR_TX, 0)
        for t in tl:
            txfs.append((t.minimum(), t.maximum(), t.step()))
        return {'rx': rxfs,
            'tx': txfs}

    def listBandwidths(self):
        return {'rx': self.sdr.listBandwidths(SOAPY_SDR_RX, 0),
            'tx': self.sdr.listBandwidths(SOAPY_SDR_TX, 0)}

    def listSampleRates(self):
        return {'rx': self.sdr.listSampleRates(SOAPY_SDR_RX, 0),
            'tx': self.sdr.listSampleRates(SOAPY_SDR_TX, 0)}

    def listClockSources(self):
        return self.sdr.listClockSources()

    def setRxSampleRate(self, rate):
        self.sdr.setSampleRate(SOAPY_SDR_RX, 0, rate)

    def setTxSampleRate(self, rate):
        self.sdr.setSampleRate(SOAPY_SDR_TX, 0, rate)

    def getRxSampleRate(self):
        return self.sdr.getSampleRate(SOAPY_SDR_RX,0)

    def getTxSampleRate(self):
        return self.sdr.getSampleRate(SOAPY_SDR_TX,0)

    def setRxFrequency(self, f):
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, f)
    
    def getRxFrequency(self):
        return self.sdr.getFrequency(SOAPY_SDR_RX, 0)
    
    def setTxFrequency(self, f):
        self.sdr.setFrequency(SOAPY_SDR_TX, 0, f)
    
    def getTxFrequency(self):
        return self.sdr.getFrequency(SOAPY_SDR_TX, 0)


    def hasRxStream(self):
        return self.rxStream is not None

    def createRxStream(self):
        if not self.hasRxStream():
            print "Creating RX stream"
            self.rxStream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
   
    def rxStreamIsActive(self):
        if self.hasRxStream():
            return self.rxStreamActiveState
        return False
        
    def activateRxStream(self):
        if self.hasRxStream():
            if not self.rxStreamActiveState:
                print "Activating RX stream"
                s = self.sdr.activateStream(self.rxStream)
                if s == 0:
                    self.rxStreamActiveState = True
                else:
                    print "Error activating stream"
        else:
            print "No rxstream"
        return self.rxStreamActiveState

    def getRxSamples(self, n):
        if self.rxStream is None:
            self.createRxStream()
        if not self.rxStreamIsActive():
            self.activateRxStream()
        buff = np.array([0]*int(n), np.complex64)
        #print "Reading"
        sr = self.sdr.readStream(self.rxStream, [buff], len(buff))
        if sr.ret < 0:
            print "ERROR while reading samples"
        #print sr
        #print buff
        return buff

#tx
    def hasTxStream(self):
        return self.txStream is not None

    def createTxStream(self):
        if not self.hasTxStream():
            print "Creating TX stream"
            self.txStream = self.sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
   
    def txStreamIsActive(self):
        if self.hasTxStream():
            return self.txStreamActiveState
        return False
        
    def activateTxStream(self):
        if self.hasTxStream():
            if not self.txStreamActiveState:
                print "Activating TX stream"
                s = self.sdr.activateStream(self.txStream)
                if s == 0:
                    self.txStreamActiveState = True
                else:
                    print "Error activating stream"
        return self.txStreamActiveState

    def putTxSamples(self, samples):
        if self.txStream is None:
            self.createTxStream()
        if not self.txStreamIsActive():
            self.activateTxStream()
        #buff = np.array([0]*int(n), np.complex64)
        sr = self.sdr.writeStream(self.txStream, [samples], len(samples))
        #sr = self.sdr.readStream(self.rxStream, [buff], len(buff))
        if sr < 0:
            #print "ERROR while writing samples"
            return []
        #print sr
        return sr



print "dfsdf",SOAPY_SDR_TIMEOUT 
#enumerate devices
results = SoapySDR.Device.enumerate()
print "Got", len(results), "devices"
devs = []
for result in results:
    print result
    devs.append(SdrDevice(result))

try:
    if True:
        for d in devs:
            d = SdrDevice({'driver':'hackrf'})
            print d
            d.setSampleRate(1e6)
            print "Sample rates", d.getSampleRate()
            d.setFrequency(145e6)
            print "Center frequencies", d.getFrequency()
            for a in range(30000):
                s = d.getRxSamples(32768/8)
                #print len(s)
                kivyPlot.plot(np.abs(np.fft.fftshift(np.fft.fft(s-np.mean(s)))))
                #if len(s):
                #    kivyPlot.plot(np.real(s))
                #plt.hold(False)
                #plt.plot(s)
                #plt.draw()
                #plt.pause(0.02)
                #print "Number of samples read", len(s)
                #print np.sum(s)
            for a in range(20):
                stat = d.putTxSamples(s)
                print stat
except KeyboardInterrupt:
    kivyPlot.stop()
    kivyPlot.join();
    exit(0)

#for dev in devs:
#   print dev.getDeviceDescription()
#   print dev
    #prin dir(dev.getDeviceDescription()['frequencies']['rx'][0])
    #print dev.getDeviceDescription()['frequencies']['rx'][0]
    #print dev.getDeviceDescription()['frequencies']['rx'].index
    #for a in dir(dev.sdr):
    #   if 'list' in a or 'get' in a:
    #       print a
    #print dev.bbdev.values()
    #print dev.bbdev.items()

#exit(0)
    #print(reSult)

#create device instance
#args can be user defined or from the enumeration result
#args = dict(driver="hackrf")
sdr = SoapySDR.Device({'driver':'hackrf'})

#query device info
#print(sdr.listAntennas(SOAPY_SDR_RX, 0))
#print(sdr.listGains(SOAPY_SDR_RX, 0))
#freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
#for freqRange in freqs: print("F"+str(freqRange))

print "Setting up rtx"
#apply settings
sdr.setSampleRate(SOAPY_SDR_RX, 0, 1e6)
sdr.setFrequency(SOAPY_SDR_RX, 0, 99.4e7)
#sdr.setSampleRate(SOAPY_SDR_TX, 0, 1e6)
#sdr.setFrequency(SOAPY_SDR_TX, 0, 99.4e7)

print "Setting up streams"
#setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
#txStream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream) #start streaming

#create a re-usable buffer for rx samples
buff = np.array([0]*8192, np.complex64)
print "receiving"
#receive some samples
plt.show()
for i in range(10):
    sr = sdr.readStream(rxStream, [buff], len(buff))
    plt.hold(False)
    plt.plot(np.abs(np.fft.fftshift(np.fft.fft(buff))))
    plt.draw()
    plt.pause(0.002)
    #print(sr.ret) #num samples or error code
    #print(sr.flags) #flags set by receive operation
    #print(sr.timeNs) #timestamp for receive buffer
#plt.plot( np.real(buff))
plt.show()
#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming
print "transmitting"
sdr.activateStream(txStream)
for i in range(1000):
    sr = sdr.writeStream(txStream, [buff], len(buff))
    print sr
sdr.deactivateStream(txStream)
sdr.closeStream(txStream)
sdr.closeStream(rxStream)
