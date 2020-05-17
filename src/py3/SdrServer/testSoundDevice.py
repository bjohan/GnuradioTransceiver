import numpy as np
import threading
import time
from . import kivyPlot
from . import soundDevice

print("Creating sound device")
d  = soundDevice.SoundDevice()
cs = 0;
def generateSamples():
    global d
    global cs
    while True:
        tv = np.linspace(cs,cs+8191,8192);
        yv = np.sin(tv/10.0)*0.1
        d.putSamples(np.vstack((yv, yv)).T)
        cs += 8192
        time.sleep(0.1)

fig = kivyPlot.Figure()
thr = threading.Thread(target=generateSamples)
thr.start()
try:
    while True:
        #plt.hold(False)
        s = d.getSamples(32768)
        if s != []:
            #print "plot", s
            fig.plot(s)
            #plt.plot(s)
            #plt.draw()
            #plt.pause(0.000001)
        else:
            time.sleep(0.001)
except KeyboardInterrupt:
    print("Control-C pressed, shuting down")


#print "Waiting for thread to join"
#time.sleep(3)
fig.stop()
d.stop()
d.join()
#print "Done"
fig.join()
