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
import time



def openSdr():
    d = soapySdrDevice.SoapySdrManager()

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
    return sdr
        
        
#sdr = openSdr()
print "Creating sound device"
sndDev  = soundDevice.SoundDevice()

print "Setting up processors"
sndsrc = soundSourceProcessor.SoundSourceProcessor(sndDev, 1024);
sndsink = soundSinkProcessor.SoundSinkProcessor(sndDev);
plotdsp = plotSignalProcessor.PlotSignalProcessor("AF time");
plotfft = fftPlotSignalProcessor.FftPlotSignalProcessor("AF freq")
statdsp = statusSignalProcessor.StatusSignalProcessor()

dsp = dspPipeLine.DspPipeLine([ [sndsrc], [plotdsp], [plotfft], [sndsink], [statdsp]])

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
        

