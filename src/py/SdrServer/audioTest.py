#import sounddevice as sd
#sd.default.samplerate = 44000
#sd.default.channels = 2
#print "Sample frequency", sd.default.samplerate
#print str(sd.default)
#fs = sd.default.samplerate
#print "Recording at", fs
#rec = sd.rec(3*fs)
#sd.wait()
#print "Done"
#print rec
#print "playback"
#sd.play(rec,fs)
#sd.wait()

import sounddevice as sd
duration = 5.5  # seconds

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

with sd.Stream(channels=2, callback=callback):
    sd.sleep(int(duration * 1000))

