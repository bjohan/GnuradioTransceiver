import numpy as np
import dspPipe
import soapySdrDevice
import dspPipeLine
import soundDevice
import dsp.source
import dsp.sink
import dsp.plot
import dsp.fftPlot
import dsp.status
import dsp.resample
import dsp.printer
import dsp.fir
import dsp.fmMod
import dsp.agc
import dsp.squelch
import time


class SineSource:
    def __init__(self):
        self.tlast = 0.0
        self.rate = 44000.0
        self.freq = 440.0#self.rate/512
        self.amplitude = 1
        pass

    def getSamples(self, nsample):
        t = np.arange(nsample)/self.rate+1.0/self.rate+self.tlast
        samples = np.exp(1.0j*np.pi*2.0*self.freq*t)
        self.tlast = t[-1]
        time.sleep(0.98*float(nsample)/float(self.rate))
        return samples*self.amplitude

def openSdr():
    d = soapySdrDevice.SoapySdrManager()

    for sdr in d.getSdrs():
        it = sdr.getItems()
        if 'driver' in it:
            if it['driver'] == 'hackrf':
                break
    else:
        print("No hackrf found. Exiting")
        exit(-1)
    sdr.setSampleRate(4e6)
    print("Sample rates", sdr.getSampleRate())
    sdr.setFrequency(145.00e6)
    print("Center frequencies", sdr.getFrequency())
    return sdr
        
        
sdr = openSdr()
print("Creating sound device")
sndDev  = soundDevice.SoundDevice()

print("Setting up processors")
sndsrc = dsp.source.Source(sndDev, samples=512, fc = 0, rate = 44000);
squelch = dsp.squelch.Squelch(threshold=0.2, hold = 0.2)
agcproc = dsp.agc.Agc(rate = 0.01*5)
fir = dsp.fir.Fir(taps = 128, passBand = 0.1, transition = 0.01)
fmmod = dsp.fmMod.FmMod(6000)
plotdsp = dsp.plot.Plot("AF time");
plotfilt = dsp.plot.Plot("Filtered");
plotfft = dsp.fftPlot.FftPlot("AF freq", nmax = 2048)
plotfm = dsp.plot.Plot("FM time");
plotfftfm = dsp.fftPlot.FftPlot("FM freq", nmax = 2048)
rfplotdsp = dsp.plot.Plot("RF time");
rfplotfft = dsp.fftPlot.FftPlot("RF freq",nmax=2048)
resamp = dsp.resample.Resample(outputRate = 4e6)
sink = dsp.sink.Sink(sdr)
statdsp = dsp.status.Status()
dsp = dspPipeLine.DspPipeLine([ [sndsrc],[plotdsp],[plotfft], [fir],[plotfilt],[squelch], [fmmod] , [plotfm], [plotfftfm], [resamp], [rfplotdsp], [rfplotfft], [sink], [statdsp]])
#dsp = dspPipeLine.DspPipeLine([ [sndsrc],[resamp],[sink]])
print("starting pipeline")
dsp.start()
try:
    while True:
        time.sleep(10)
        dsp.status()
except KeyboardInterrupt:
    print("stopping dsp pipeline")
    dsp.stop()
    sndDev.stop()
exit(0)
        

