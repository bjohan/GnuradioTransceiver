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
        self.txStreamActiveState = True;
        self.rxStream = None
        self.txStream = None
    
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
        return self.rxStreamActiveState

    def getRxSamples(self, n):
        if self.rxStream is None:
            self.createRxStream()
        if not self.rxStreamIsActive():
            self.activateRxStream()
        buff = np.array([0]*int(n), np.complex64)
        sr = self.sdr.readStream(self.rxStream, [buff], len(buff))
        if sr < 0:
            print "ERROR while reading samples"
        print sr
        return buff
   
#enumerate devices
results = SoapySDR.Device.enumerate()
print "Got", len(results), "devices"
devs = []
for result in results:
    devs.append(SdrDevice(result))


for d in devs:
    print d
    d.setSampleRate(1e6)
    print "Sample rates", d.getSampleRate()
    d.setFrequency(99.4e6)
    print "Center frequencies", d.getFrequency()
    s = d.getRxSamples(10e3)
    print "Number of samples read", len(s)
    print np.sum(s)
exit(0)

#for dev in devs:
#   print dev.getDeviceDescription()
#   print dev
    #print dir(dev.getDeviceDescription()['frequencies']['rx'][0])
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
print(sdr.listAntennas(SOAPY_SDR_RX, 0))
print(sdr.listGains(SOAPY_SDR_RX, 0))
freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
for freqRange in freqs: print("F"+str(freqRange))

#apply settings
sdr.setSarpleRate(SOAPY_SDR_RX, 0, 1e6)
sdr.setFrequency(SOAPY_SDR_RX, 0, 99.4e6)
sdr.setSampleRate(SOAPY_SDR_TX, 0, 1e6)
sdr.setFrequency(SOAPY_SDR_TX, 0, 99.4e6)

#setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
txStream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream) #start streaming

#create a re-usable buffer for rx samples
buff = numpy.array([0]*1024, numpy.complex64)

#receive some samples
for i in range(1000):
    sr = sdr.readStream(rxStream, [buff], len(buff))
    #print(sr.ret) #num samples or error code
    #print(sr.flags) #flags set by receive operation
    #print(sr.timeNs) #timestamp for receive buffer

#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming

sdr.activateStream(txStream)
for i in range(1000):
    sr = sdr.writeStream(txStream, [buff], len(buff))
    #print sr
sdr.deactivateStream(txStream)
sdr.closeStream(txStream)
sdr.closeStream(rxStream)
