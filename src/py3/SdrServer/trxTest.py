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
import dsp.fft
import dsp.db
import dsp.limiter
import dsp.fmDemod
import dsp.tuner
import dsp.squelch
import dsp.acCouple

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
txplotdsp = dsp.plot.Plot("TX AF time");
txplotfilt = dsp.plot.Plot("TX Filtered");
txplotfft = dsp.fftPlot.FftPlot("TX AF freq", nmax = 2048)
txplotfm = dsp.plot.Plot("TX FM time");
txplotfftfm = dsp.fftPlot.FftPlot("TX FM freq", nmax = 2048)
txrfplotdsp = dsp.plot.Plot("TX RF time");
txrfplotfft = dsp.fftPlot.FftPlot("TX RF freq",nmax=2048)
txresamp = dsp.resample.Resample(outputRate = 4e6)
txsink = dsp.sink.Sink(sdr)
txstatdsp = dsp.status.Status()
txdsp = dspPipeLine.DspPipeLine([ [txsndsrc],[txplotdsp],[txplotfft], [txfir],[txplotfilt],[txsquelch], [txfmmod] , [txplotfm], [txplotfftfm], [txresamp], [txrfplotdsp], [txrfplotfft], [txsink], [txstatdsp]])


rxsdrsrc = dsp.source.Source(sdr, samples = 32768, fc = sdr.getFrequency()['rx'], rate = sdr.getSampleRate()['rx'])
rxfirdsp = dsp.fir.Fir(taps = 256, passBand=0.00001);
rxfmdsp = dsp.fmDemod.FmDemod()
rxagcdsp = dsp.agc.Agc(target=1, maxAmp = 10, rate =0.01)
rxfftdsp = dsp.fft.Fft(samples=4096)
rxdbdsp = dsp.db.Db()
rxdecdsp = dsp.resample.Resample(outputRate=44000)
rxlimitdsp = dsp.limiter.Limiter(mi=-1, ma = 1)
rxsndsink = dsp.sink.Sink(sndDev);
rxplotdsp = dsp.plot.Plot("RX Demodulated fm");
rxplotfm = dsp.plot.Plot("RX decimated td");
rxplotfft = dsp.fftPlot.FftPlot("RX Decimated spectrum", nmax = 512)
rxplotfftfull = dsp.fftPlot.FftPlot("RX full spectrum", nmax = 512)
rxplotfftfir = dsp.fftPlot.FftPlot("RX firfiltered full spectrum", nmax=512)
rxsquelch = dsp.squelch.Squelch(threshold = 0.01, hold = 0.00000)
rxac = dsp.acCouple.AcCouple()
rxac2 = dsp.acCouple.AcCouple()

rxstatdsp = dsp.status.Status()
rxdsp = dspPipeLine.DspPipeLine([ [rxsdrsrc], [rxac], [rxplotfftfull], [rxfirdsp],[rxplotfftfir], [rxdecdsp], [rxplotfft], [rxplotfm], [rxsquelch], [rxfmdsp],[rxac2], [rxplotdsp], [rxagcdsp],[rxsndsink], [rxstatdsp]])

print("starting tx pipeline")
txdsp.start()
print("starting rx pipeline")
rxdsp.start()
try:
    while True:
        time.sleep(10)
        dsp.status()
except KeyboardInterrupt:
    print("stopping dsp pipeline")
    rxdsp.stop()
    txdsp.stop()
    sndDev.stop()
exit(0)
        

