import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers


class SdrDeviceBase:
	#Class that will service each baseband device
	def __init__(self):
		pass
	
	def getDeviceIdentifier(self):
		print "Warning unimplemented getDeviceIdentifier"
		return {}

	def getDeviceIdentifierString(self):
		return "Unimplemented getDeviceIdentifierString" 

	def listAntennas(self):
		print "Warning unimplemented listAntennas"
		return {}
	

	def listGains(self):
		print "Warning unimplemented listGains"
		return {}
		
	def listFreqs(self):
		print "Warning unimplemented listFreqs"
		return {}

	def listBandwidths(self):
		print "Warning unimplemented listBandwidth"
		return {}

	def listSampleRates(self):
		print "Warning unimplemented listSampleRates"
		return {}

	def listClockSources(self):
		print "Warning unimplemented listClockSources"
		return []

        def setRxSampleRate(self, rate):
            print "Warning, unimplemented setRxSampleRate"
            return false

        def getRxSampleRate(self, rate):
            print "Warning, unimplemented getRxSampleRate"
            return 0

        def setSampleRate(self, rate):
            r = self.setRxSampleRate(rate)
            t = self.setTxSampleRate(rate)
            return (r,t)
	
        def setTxSampleRate(self):
            print "Warning, unimplemented setTxSampleRate"
            return false

        def getTxSampleRate(self):
            print "Warning, unimplemented getTxSampleRate"
            return 0

        def getSampleRate(self):
            return {'rx':self.getRxSampleRate(), 'tx':self.getTxSampleRate()}

        def setTxFrequency(self, f):
           print "Warning, unimplemented setTxFrequency"
           return false

        def getTxFrequency(self, f):
           print "Warning, unimplemented getTxFrequency"
           return false

        def setRxFrequency(self, f):
           print "Warning, unimplemented setRxFrequency"
           return 0

        def getRxFrequency(self, f):
           print "Warning, unimplemented getRxFrequency"
           return 0

        def getFrequency(self):
            return {'rx':self.getRxFrequency(), 'tx':self.getTxFrequency()}

        def setFrequency(self, f):
            self.setRxFrequency(f)
            self.setTxFrequency(f)

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
		ret+=str(self.getDeviceIdentifierString())

		ret+='\n'
		return ret

