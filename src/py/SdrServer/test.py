import numpy as np
import dspPipe
import soapySdrDevice
import sdrSourceProcessor
import fftSignalProcessor
import firSignalProcessor
import plotSignalProcessor
import dbSignalProcessor
import limitSignalProcessor
import decimationSignalProcessor
import agcSignalProcessor
import fmDemodSignalProcessor
import soundSinkProcessor
import dspPipeLine
import time
import soundDevice
import fftPlotSignalProcessor

d = soapySdrDevice.SoapySdrManager()

#list all sdr devices
print "SDR devices"
for s in d.getSdrs():
	print "Device", str(s)

for sdr in d.getSdrs():
    it = sdr.getItems()
    if 'driver' in it:
        if it['driver'] == 'hackrf':
            break
else:
    print "No hackrf found. Exiting"
    exit(-1)
        
        
sdr.setSampleRate(2e6)
print "Sample rates", sdr.getSampleRate()
sdr.setFrequency(145.00e6)
print "Center frequencies", sdr.getFrequency()

print "Creating sound device"
sndDev  = soundDevice.SoundDevice()

print "Setting up processors"
sdrsrc = sdrSourceProcessor.SdrSourceProcessor(sdr, samples = 32768)
firdsp = firSignalProcessor.FirSignalProcessor(taps = 31, passBand=0.1);
fmdsp = fmDemodSignalProcessor.FmDemodSignalProcessor()
agcdsp = agcSignalProcessor.AgcSignalProcessor(target=0.1, rate = 0)
fftdsp = fftSignalProcessor.FftSignalProcessor(samples=4096)
dbdsp = dbSignalProcessor.DbSignalProcessor()
decdsp = decimationSignalProcessor.DecimationSignalProcessor(factor=137)
limitdsp = limitSignalProcessor.LimitSignalProcessor(mi=-0.0)
sndsink = soundSinkProcessor.SoundSinkProcessor(sndDev);
plotdsp = plotSignalProcessor.PlotSignalProcessor();
plotfft = fftPlotSignalProcessor.FftPlotSignalProcessor()

dsp = dspPipeLine.DspPipeLine([ [sdrsrc], [firdsp], [decdsp], [plotfft], [fmdsp], [plotdsp]])# [agcdsp], [sndsink], [fftdsp], [dbdsp, limitdsp], [plotdsp]])

print "starting pipeline"
dsp.start()
#sdrpipe.start()
try:
    while True:
        time.sleep(1)
        dsp.status()
except KeyboardInterrupt:
    print "stopping dsp pipeline"
    dsp.stop()
    sndDev.stop()
exit(0)
try:
    while True:
        ns = 32768/8
        ttot = time.time()
        tget = time.time()
        s = sdrprocessor.process(None) #sdr.getRxSamples(ns)
        tget = time.time()-tget

        tfilt = time.time()
        filt = firdsp.process(s)
        tfilt = time.time()-tfilt
    
        tfft = time.time()
        freqd = fftdsp.process(filt)
        tfft = time.time()-tfft

        tabs = time.time()
        absd = np.abs(freqd)
        tabs = time.time()-tabs


        tplot = time.time()
        #kivyPlot.plot(absd)
        plotdsp.process(absd)
        tplot = time.time()-tplot
        ttot = time.time()-ttot
        print "get", tget, "filt", tfilt, "fft", tfft, "abs", tabs, "plot", tplot, "tot", ttot, "rate", float(ns)/ttot
except KeyboardInterrupt:
    pass
#    kivyPlot.stop()
#    kivyPlot.join()
        

