import numpy as np
import dspPipe
import soapySdrDevice
import plotSignalProcessor
import dspPipeLine
import soundDevice
import fftPlotSignalProcessor
import statusSignalProcessor
import soundSourceProcessor
import soundSinkProcessor
import resamplingSignalProcessor
import time
import dspSignal

class SineSource:
    def __init__(self):
        pass

    def getSamples(self, nsample):
        o = time.time()*1.1
        samples = np.sin(np.linspace(o,((4*np.pi)*(nsample-1)/nsample)+o, nsample)) 
        return samples

        
sigsrc = SineSource()

print "Setting up processors"
sndsrc = soundSourceProcessor.SoundSourceProcessor(sigsrc, 16);
plotdsp = plotSignalProcessor.PlotSignalProcessor("AF time ");
plotfft = fftPlotSignalProcessor.FftPlotSignalProcessor("AF freq")
decdsp = resamplingSignalProcessor.ResamplingSignalProcessor(44000*512*2*2*2); 
plotdspd = plotSignalProcessor.PlotSignalProcessor("AF time decim");
plotfftd = fftPlotSignalProcessor.FftPlotSignalProcessor("AF freq decim", nmax = 512)
statdsp = statusSignalProcessor.StatusSignalProcessor()
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
        

