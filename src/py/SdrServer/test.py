import soapySdrDevice

d = soapySdrDevice.SoapySdrManager()

for s in d.getSdrs():
	print "Device", str(s)
