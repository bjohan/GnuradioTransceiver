import matplotlib.pyplot as plt
import numpy as np
import srtmData
import heightResampler

sd = srtmData.SrtmData()
hr = heightResampler.HeightResampler(sd)

e, x, y = sd.getBlock(12, 57)
print x
print y
#plt.figure(1)
#plt.imshow(np.clip(e, 0, 10000), extent=[x[0], x[-1], y[-1], y[0]])
plt.figure(2)

xr = np.linspace(-180,180,500*2)
yr = np.linspace(-60,60,500)
#xr = np.linspace(12,14,500)
#yr = np.linspace(57,59,500)

#australia
#xr = np.linspace(110,155,10000)
#yr = np.linspace(-45,-10,5000)


rs = hr.get(xr, yr)
plt.imshow(np.clip(rs,0,10000), extent=[xr[0], xr[-1], yr[0], yr[-1]])
plt.show()
