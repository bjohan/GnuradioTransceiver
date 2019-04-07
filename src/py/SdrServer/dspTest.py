import numpy as np
import dspPipe
import soapySdrDevice
import dspPipeLine
import soundDevice
#import plotSignalProcessor
#import fftPlotSignalProcessor
#import statusSignalProcessor
#import soundSourceProcessor
#import soundSinkProcessor
#import resamplingSignalProcessor
import time
#import dspSignal
import dsp.source
import dsp.plot
import dsp.fftPlot
import dsp.status
import dsp.resample
class SineSource:
    def __init__(self):
        pass

    def getSamples(self, nsample):
        o = time.time()*1.1
        samples = np.sin(np.linspace(o,((4*np.pi)*(nsample-1)/nsample)+o, nsample))
        time.sleep(0.001)
        return samples

        
sigsrc = SineSource()

print "Setting up processors"
sndsrc = dsp.source.Source(sigsrc, fc = 0, rate = 44000, samples=16);
plotdsp = dsp.plot.Plot("AF time ");
plotfft = dsp.fftPlot.FftPlot("AF freq", nmax = 512)
decdsp = dsp.resample.Resample(44000*512*2*2*2); 
plotdspd = dsp.plot.Plot("AF time decim");
plotfftd = dsp.fftPlot.FftPlot("AF freq decim", nmax = 512)
statdsp = dsp.status.Status()
dsp = dspPipeLine.DspPipeLine([ [sndsrc], [plotdsp], [plotfft], [decdsp], [plotdspd], [plotfftd],[statdsp]])

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
        

