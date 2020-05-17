class SdrManager:
	#Class that mangages multiple SDR devices
	def __init__(self):
		self.managers = []
		self.sdrs = []

	def addManager(self, mgr):
		self.managers.append(mgr)

	def addSdr(self, sdr):
		self.sdrs.append(sdr)

	def getSdrs(self):
		ret = []
		for m in self.managers:
			ret+=m.getSdrs()
		
		ret+=self.sdrs
		return ret
