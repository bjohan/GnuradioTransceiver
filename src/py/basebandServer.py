import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers

#enumerate devices
results = SoapySDR.Device.enumerate()
print "Got", len(results), "devices"
for result in results: print(result)

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
sdr.setSampleRate(SOAPY_SDR_RX, 0, 1e6)
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
for i in range(10000):
    sr = sdr.readStream(rxStream, [buff], len(buff))
    #print(sr.ret) #num samples or error code
    #print(sr.flags) #flags set by receive operation
    #print(sr.timeNs) #timestamp for receive buffer

#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming

sdr.activateStream(txStream)
for i in range(10000):
	sr = sdr.writeStream(txStream, [buff], len(buff))
	#print sr
sdr.deactivateStream(txStream)
sdr.closeStream(txStream)
sdr.closeStream(rxStream)
