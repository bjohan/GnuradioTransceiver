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
sndsrc = dsp.source.Source(sndDev, samples=1024*2, fc = 0, rate = 44000);
sndsink = dsp.sink.Sink(sndDev);
printer = dsp.printer.Printer()
plotdsp = dsp.plot.Plot("AF time");
plotfft = dsp.fftPlot.FftPlot("AF freq")
statdsp = dsp.status.Status()
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
        

