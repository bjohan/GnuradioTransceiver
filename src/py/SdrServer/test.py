import numpy as np
import dspPipe
import soapySdrDevice
import dsp.source
import dsp.fft
import dsp.fir
import dsp.plot
import dsp.db
import dsp.limiter
import dsp.resample
import dsp.agc
import dsp.fmDemod
import dsp.sink
import dspPipeLine
import time
import soundDevice
import dsp.fftPlot
import dsp.status
import dsp.tuner
import dsp.squelch
import dsp.acCouple


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
sdrsrc = dsp.source.Source(sdr, samples = 32768, fc = sdr.getFrequency()['rx'], rate = sdr.getSampleRate()['rx'])
firdsp = dsp.fir.Fir(taps = 256, passBand=0.00001);
fmdsp = dsp.fmDemod.FmDemod()
agcdsp = dsp.agc.Agc(target=1, maxAmp = 10, rate =0.01)
fftdsp = dsp.fft.Fft(samples=4096)
dbdsp = dsp.db.Db()
decdsp = dsp.resample.Resample(outputRate=44000)
limitdsp = dsp.limiter.Limiter(mi=-1, ma = 1)
sndsink = dsp.sink.Sink(sndDev);
plotdsp = dsp.plot.Plot("Demodulated fm");
plotfm = dsp.plot.Plot("decimated td");
plotfft = dsp.fftPlot.FftPlot("Decimated spectrum", nmax = 512)
plotfftfull = dsp.fftPlot.FftPlot("full spectrum", nmax = 512)
plotfftfir = dsp.fftPlot.FftPlot("firfiltered full spectrum", nmax=512)
squelch = dsp.squelch.Squelch(threshold = 0.01, hold = 0.00000)
ac = dsp.acCouple.AcCouple()
ac2 = dsp.acCouple.AcCouple()

statdsp = dsp.status.Status()
tunedsp = dsp.tuner.Tuner(nco=-1500)
dsp = dspPipeLine.DspPipeLine([ [sdrsrc], [ac], [plotfftfull], [firdsp],[plotfftfir], [decdsp],[tunedsp], [plotfft], [plotfm], [squelch], [fmdsp],[ac2], [plotdsp], [agcdsp],[sndsink], [statdsp]])# [agcdsp], [sndsink], [fftdsp], [dbdsp, limitdsp], [plotdsp]])

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
        

