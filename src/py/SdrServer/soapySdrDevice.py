import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import sdrDevice
import sdrManager

class SoapySdrDevice(sdrDevice.SdrDeviceBase):
	#Class that will service each baseband device
	def __init__(self, bbdev):
		
		self.bbdev = bbdev
		self.sdr = SoapySDR.Device(bbdev)


	def mapToDict(self, m):
		d = {}
		for k in m.keys():
			d[k] = m[k]
		return d

	def getDeviceIdentifier(self):
		return {'hardware_info':self.mapToDict(self.sdr.getHardwareInfo()),
			 'driver': self.sdr.getDriverKey()}
	
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
			'clock_sources': self.listClockSources(),
			'device_identifier': self.getDeviceIdentifier()}

	def getDeviceIdentifierString(self):
		di = self.getDeviceIdentifier()
		return "Driver: %s driver specific: %s\n"%(di['driver'], str(di['hardware_info']))


class SoapySdrManager(sdrManager.SdrManager):
	def __init__(self):
		sdrManager.SdrManager.__init__(self)
		results = SoapySDR.Device.enumerate()
		for result in results:
			self.addSdr(SoapySdrDevice(result))

	
