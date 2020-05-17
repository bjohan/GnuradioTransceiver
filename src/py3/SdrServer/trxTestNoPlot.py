import numpy as np
from . import dspPipe
from . import soapySdrDevice
from . import dspPipeLine
from . import soundDevice
from . import dsp.source
from . import dsp.sink
from . import dsp.status
from . import dsp.resample
from . import dsp.printer
from . import dsp.fir
from . import dsp.fmMod
from . import dsp.agc
from . import dsp.squelch
import time
from . import dsp.fft
from . import dsp.db
from . import dsp.limiter
from . import dsp.fmDemod
from . import dsp.tuner
from . import dsp.squelch
from . import dsp.acCouple

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

print("Setting up processors for tx pipe")
txsndsrc = dsp.source.Source(sndDev, samples=512, fc = 0, rate = 44000);
txsquelch = dsp.squelch.Squelch(threshold=0.2, hold = 0.2)
txagcproc = dsp.agc.Agc(rate = 0.01*5)
txfir = dsp.fir.Fir(taps = 128, passBand = 0.1, transition = 0.01)
txfmmod = dsp.fmMod.FmMod(6000)
txresamp = dsp.resample.Resample(outputRate = 4e6)
txsink = dsp.sink.Sink(sdr)
txstatdsp = dsp.status.Status()
txdsp = dspPipeLine.DspPipeLine([ [txsndsrc], [txfir],[txsquelch], [txfmmod] , [txresamp], [txsink], [txstatdsp]])


rxsdrsrc = dsp.source.Source(sdr, samples = 32768, fc = sdr.getFrequency()['rx'], rate = sdr.getSampleRate()['rx'])
rxfirdsp = dsp.fir.Fir(taps = 256, passBand=0.00001);
rxfmdsp = dsp.fmDemod.FmDemod()
rxagcdsp = dsp.agc.Agc(target=1, maxAmp = 10, rate =0.01)
rxfftdsp = dsp.fft.Fft(samples=4096)
rxdbdsp = dsp.db.Db()
rxdecdsp = dsp.resample.Resample(outputRate=44000)
rxlimitdsp = dsp.limiter.Limiter(mi=-1, ma = 1)
rxsndsink = dsp.sink.Sink(sndDev);
rxsquelch = dsp.squelch.Squelch(threshold = 0.01, hold = 0.00000)
rxac = dsp.acCouple.AcCouple()
rxac2 = dsp.acCouple.AcCouple()

rxstatdsp = dsp.status.Status()
rxdsp = dspPipeLine.DspPipeLine([ [rxsdrsrc], [rxac], [rxfirdsp], [rxdecdsp],[rxsquelch], [rxfmdsp],[rxac2], [rxagcdsp],[rxsndsink], [rxstatdsp]])

print("starting tx pipeline")
txdsp.start()
print("starting rx pipeline")
rxdsp.start()
try:
    while True:
        time.sleep(10)
        txdsp.status()
        rxdsp.status()
except KeyboardInterrupt:
    print("stopping dsp pipeline")
    rxdsp.stop()
    txdsp.stop()
    sndDev.stop()
exit(0)
        

