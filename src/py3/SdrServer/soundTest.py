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


print("Creating sound device")
sndDev  = soundDevice.SoundDevice()

print("Setting up processors")
sndsrc = dsp.source.Source(sndDev, samples=512, fc = 0, rate = 44000);
sndsnk = dsp.sink.Sink(sndDev);
plot = dsp.plot.Plot("AF time");
plotFrequency = dsp.fftPlot.FftPlot("AF frequency");
statdsp = dsp.status.Status()
dsp = dspPipeLine.DspPipeLine([ [sndsrc],[plot], [plotFrequency],[sndsnk], [statdsp]])
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
        

