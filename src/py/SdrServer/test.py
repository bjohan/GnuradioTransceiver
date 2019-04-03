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
import statusSignalProcessor
import tuneSignalProcessor
import squelchSignalProcessor


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
        
        
sdr.setSampleRate(4e6)
print "Sample rates", sdr.getSampleRate()
sdr.setFrequency(145.00e6)
print "Center frequencies", sdr.getFrequency()

print "Creating sound device"
sndDev  = soundDevice.SoundDevice()

print "Setting up processors"
sdrsrc = sdrSourceProcessor.SdrSourceProcessor(sdr, samples = 32768, fc = sdr.getFrequency()['rx'], rate = sdr.getSampleRate()['rx'])
firdsp = firSignalProcessor.FirSignalProcessor(taps = 31, passBand=0.1);
fmdsp = fmDemodSignalProcessor.FmDemodSignalProcessor()
agcdsp = agcSignalProcessor.AgcSignalProcessor(target=1, maxAmp = 10, rate =0.01)
fftdsp = fftSignalProcessor.FftSignalProcessor(samples=4096)
dbdsp = dbSignalProcessor.DbSignalProcessor()
decdsp = decimationSignalProcessor.DecimationSignalProcessor(factor=91)
limitdsp = limitSignalProcessor.LimitSignalProcessor(mi=-1, ma = 1)
sndsink = soundSinkProcessor.SoundSinkProcessor(sndDev);
plotdsp = plotSignalProcessor.PlotSignalProcessor("Demodulated fm");
plotfm = plotSignalProcessor.PlotSignalProcessor("decimated td");
plotfft = fftPlotSignalProcessor.FftPlotSignalProcessor("Decimated spectrum", nmax = 512)
plotfftfull = fftPlotSignalProcessor.FftPlotSignalProcessor("full spectrum", nmax = 512)
plotfftfir = fftPlotSignalProcessor.FftPlotSignalProcessor("firfiltered full spectrum", nmax=512)
squelch = squelchSignalProcessor.SquelchSignalProcessor(threshold = 0.4, hold = 0.00000)

statdsp = statusSignalProcessor.StatusSignalProcessor()
tunedsp = tuneSignalProcessor.TuneSignalProcessor(nco=-1500)
dsp = dspPipeLine.DspPipeLine([ [sdrsrc], [plotfftfull], [firdsp],[plotfftfir], [decdsp],[tunedsp], [plotfft], [plotfm], [squelch], [fmdsp],[plotdsp], [agcdsp],[sndsink], [statdsp]])# [agcdsp], [sndsink], [fftdsp], [dbdsp, limitdsp], [plotdsp]])

print "starting pipeline"
dsp.start()
try:
    while True:
        time.sleep(10)
        dsp.status()
except KeyboardInterrupt:
    print "stopping dsp pipeline"
    dsp.stop()
    sndDev.stop()
exit(0)
        

