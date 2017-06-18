import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers


class SdrDevice:
	#Class that will service each baseband device
	def __init__(self, bbdev):
		self.bbdev = bbdev
		self.sdr = SoapySDR.Device(bbdev)
	
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
	
	def getDeviceDescription(self):
		return {
			'antennas':self.listAntennas(),
			'gains': self.listGains(),
			'frequencies': self.listFreqs(),
			'bandwidths': self.listBandwidths(),
			'sample_rates': self.listSampleRates(),
			'clock_sources': self.listClockSources()}
	
	def rtxDictToString(self, rxtext, txtext, d):
		ret = ""
		if 'rx' in d:
			ret+=rxtext
			for p in d['rx']:
				ret += str(p)+' '
		ret+='\n'
		if 'tx' in d:
			ret+=txtext
			for p in d['tx']:
				ret += str(p)+' '

		return ret+'\n'

	def tupleToString(self, name, tup):
		ret = ''
		if len(tup):
			ret+=name
			for t in tup:
				ret+=t+' '
			ret+='\n'
		return ret
	
	def __str__(self):
		ret = "SDR device info\n"
		ret+= "="*len(ret)+'\n'
		for p in self.bbdev.items():
			ret+="%s: %s\n"%p
		ret+=self.rtxDictToString("RX antennas: ", "TX antennas: ", self.listAntennas())
		ret+=self.rtxDictToString("RX gains: ", "TX gains: ", self.listGains())
		ret+=self.rtxDictToString("RX freqs: ", "TX freqs: ", self.listFreqs())
		ret+=self.rtxDictToString("RX bw: ", "TX bw: ", self.listBandwidths())
		ret+=self.rtxDictToString("RX rates: ", "TX rates: ", self.listSampleRates())
		ret+=self.tupleToString("Clocks: ", self.listClockSources())

		ret+='\n'
		return ret

#enumerate devices
results = SoapySDR.Device.enumerate()
print "Got", len(results), "devices"
devs = []
for result in results: 
	devs.append(SdrDevice(result))
for dev in devs:
	print dev.getDeviceDescription()
	print dev
	#print dir(dev.getDeviceDescription()['frequencies']['rx'][0])
	#print dev.getDeviceDescription()['frequencies']['rx'][0]
	#print dev.getDeviceDescription()['frequencies']['rx'].index
	#for a in dir(dev.sdr):
	#	if 'list' in a or 'get' in a:
	#		print a
	#print dev.bbdev.values()
	#print dev.bbdev.items()

exit(0)
	#print(result)

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
