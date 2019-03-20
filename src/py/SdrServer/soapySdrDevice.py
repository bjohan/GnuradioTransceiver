import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import sdrDevice
import sdrManager
import numpy as np

class SoapySdrDevice(sdrDevice.SdrDeviceBase):
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
        self.sdr.setGain(SOAPY_SDR_RX, 0, 50+0*100)


    def mapToDict(self, m):
        d = {}
        for k in m.keys():
            d[k] = m[k]
        return d

    def getDeviceIdentifier(self):
        return {'hardware_info':self.mapToDict(self.sdr.getHardwareInfo()),
             'driver': self.sdr.getDriverKey()}
    
    def getDeviceDescription(self):
        return {
            'antennas':self.listAntennas(),
            'gains': self.listGains(),
            'frequencies': self.listFreqs(),
            'bandwidths': self.listBandwidths(),
            'sample_rates': self.listSampleRates(),
            'clock_sources': self.listClockSources(),
            'device_identifier': self.getDeviceIdentifier()}

    def getDeviceIdentifierString(self):
        di = self.getDeviceIdentifier()
        return "Driver: %s driver specific: %s\n"%(di['driver'], str(di['hardware_info']))


 
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
            #print "ERROR while reading samples", sr
            return None
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

    def getItems(self):
        d = {}
        for p in self.bbdev.items():
            d[p[0]]=p[1]
        return d

    def __str__(self):
        ret = sdrDevice.SdrDeviceBase.__str__(self)+'\n'
        #for p in self.bbdev.items():
        ret+=str(self.getItems())
        return ret




class SoapySdrManager(sdrManager.SdrManager):
    def __init__(self):
        sdrManager.SdrManager.__init__(self)
        results = SoapySDR.Device.enumerate()
        for result in results:
            self.addSdr(SoapySdrDevice(result))

    
