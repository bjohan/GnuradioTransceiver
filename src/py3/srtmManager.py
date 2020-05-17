import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import os
import math
import zipfile
import numpy as np
import sys
from BeautifulSoup import BeautifulSoup

class SrtmCache:
    def __init__(self, cacheDir='./srtmCache/'):
        self.cacheDir = cacheDir
        self. initCacheDir()

    def initCacheDir(self):
        if not os.path.isdir(self.cacheDir):
            os.mkdir(self.cacheDir)

    def getCacheName(self, url):
        fn = url.split('/')[-1]
        cacheEntryName = os.path.join(self.cacheDir,fn)
        return cacheEntryName

    def inCache(self, url):
        if os.path.isfile(self.getCacheName(url)):
            return True
        return False

    def getUrl(self, url):
        if not self.inCache(url):
            print("downloading", url)
            urllib.request.urlretrieve(url, self.getCacheName(url))
            #r = urllib2.urlopen(url)
            #print "Writing to file"
            #with open(self.getCacheName(url), 'w') as w:
            #        w.write(r.read())
        if self.inCache(url):
            return self.getCacheName(url)
        return None

class srtmManager:
    def __init__(self, url='https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/'):
        self.srtmIndex = 'srtmIndex.txt'
        self.url = url
        self.srtms = None
        self.prepareIndex()
        self. cache = SrtmCache()
        #self.srtms = self.scanIndex()

    def prepareIndex(self):
        self.srtms = self.scanIndex()
        #print "Srtms is", self.srtms
        if self.srtms is None:
            print("Failed to load srtm index from", self.srtmIndex, "Downloading")
            self.buildIndex()
            self.srtms = self.scanIndex()
        if self.srtms is None:
            print("ERROR, failed to create SRTM index")
        else:
            print("SRTM index was successfully loaded")

    def scanIndex(self):
        index = {}
        try:
            with open(self.srtmIndex) as idx:
                for line in idx.read().splitlines():
                    name = line.split('/')[-1].split('.')[0]
                    lon = None
                    lat = None
                    if 'W' in name:
                        #lon = int(name.split('W')[-1])
                        lon = int(name[4:7])
                    if 'E' in name:
                        #lon = 180-int(name.split('E')[-1])
                        lon = -int(name[4:7])
                    if 'N' in name:
                        l = int(name[1:3])
                        lat = l
                    if 'S' in name:
                        l = int(name[1:3])
                        lat = -l
                    #print lat, lon
                    index[(lat, lon)]= line
        except Exception as e:
            print("Failed to build srtm", self.srtmIndex, e)
            return None
        return index

    def buildIndex(self):
        files = self.downloadChildren(self.url)
        ih = open(self.srtmIndex, 'w')
        for f in files:
            ih.write(f+'\n')
        ih.close()
        
        #print files

    def downloadChildren(self, url):
        print("downloading", url)
        r = urllib.request.urlopen(url)
        files = []
        f, nodes = self.parseLinks(r.read())
        for fi in f:
            files.append(url+fi)
        for n in nodes:
            files+=self.downloadChildren(url+n)

        return files

    def parseLinks(self, page):
        s = BeautifulSoup(page)
        files = []
        nodes = []
        for link in s.findAll('a'):
            if 'Parent' not in link.getText():
                href = link.get('href')
                if '.zip' in href:
                    files.append(href)
                else:
                    nodes.append(href)
                #print link.get('href')
                #print link.getText()
        return files, nodes

    def getBlock(self, lat, lon):
        """ get a datablock containing lat and lon"""

        lat = int(lat)
        lon = int(lon) 
        L = 1201
        #Get name of the zip file containing data from cache.  
        if (int(lat), int(lon)) not in self.srtms:
            print("Lat", lat, "Lon", lon, "is probably sea")
            elevations = np.zeros((1201, 1201))
        else:
            url = self.srtms[(int(lat), int(lon))]
            cachename = self.cache.getUrl(url)
            zipname = os.path.basename(cachename)[:-4]
            print("Loading", zipname)

            #Open the zip file
            try:
                with zipfile.ZipFile(cachename) as f:
                    zipname = f.namelist()[0]
                    if f.namelist()[0]:
                        print("Loading", zipname)
                        try:
                            with f.open(zipname) as hgt:
                                elevations = np.fromstring(hgt.read(), np.dtype('>i2', L*L)).reshape((L,L))
                        except Exception as e:
                            print("Error while parsing hgt from zip", hgt, zipname, e)
                            elevations = np.zeros((1201, 1201))
                    else:
                        print(zipname, "not in", f.namelist())
                        elevations = np.zeros((1201, 1201))
            except Exception as e:
                print("Error opening zip-file", cachename, e)
        
        #Generate axis data for latitudes and longitudes
        #lonsign = np.sign(lon)
        #latsign = np.sign(lat)
        
        lonRange = np.linspace(lon, lon+1, L)
        latRange = np.linspace(lat, lat+1, L)
        
        return elevations, lonRange, latRange


    def getElevation(self, lat, lon):
        if (int(lat), int(lon)) not in self.srtms:
            return 0 #Sea level
        url = self.srtms[(int(lat), int(lon))]
        #print "Attemting to get", url, "from cache"
        cachename = self.cache.getUrl(url)
        #print lat, lon, "is in cache as", cachename
        zipname = os.path.basename(cachename)[:-4]
        idxlat = 0
        idxlon = 0
        try:
            with zipfile.ZipFile(cachename) as f:
                zipname = f.namelist()[0]
                if f.namelist()[0]:
                    print("Loading", zipname)
                    try:
                        with f.open(zipname) as hgt:
                            L = 1201
                            elevations = np.fromstring(hgt.read(), np.dtype('>i2', L*L)).reshape((L,L))
                            #print "Wiiiee", elevations.shape
                            idxlon = int(math.floor((lon-int(lon))*1200))
                            if(idxlon < 0 ):
                                idxlon = 1200+idxlon
                            idxlat = int(math.floor((lat-int(lat))*1200))
                            if(idxlat < 0 ):
                                idxlat = 1200+idxlat
                            idxlon=1200-idxlon
                            idxlat=1200-idxlat
                            #print "longitude index", idxlon, "lat", idxlat
                            #print "elevation", elevations[idxlon, idxlat]
                    except Exception as e:
                        print("Error while parsing hgt from zip", hgt, zipname, e)
                        elevations = np.zeros((1201, 1201))
                else:
                    print(zipname, "not in", f.namelist())
                    elevations = np.zeros((1201, 1201))
        except Exception as e:
            print("Error opening zip-file", cachename, e)
        e = elevations[idxlat, idxlon]
        if e < 0:
            e = 0;
        return e

class ElevationDataManager:
    def __init__(self, dataSource):
        self.ds = dataSource


    def resampleNearest(self, toResample, values):
        idx = []
        for v in toResample:
            #print "resampling", v, "boundary is", values[0], values[-1]
            if v>=values[0] and v <= values[-1]:
                #print "resampling", v
                i =  np.abs(values -v).argmin()
                idx.append(i)
        return idx
                
    def getData(self, xs, ys):
        #Ok unable to remember which is latitude and which is longitude.
        #x is longitude, and y is latitude. 
        print("x range is", xs[0], xs[-1], "yrange is", ys[0], ys[-1])
        import matplotlib.pyplot as plt
        data = np.zeros((xs.shape[0], ys.shape[0]))
        print("shape of destination is", data.shape)
        cX = xs[0]
        cY = ys[0]
        yi = len(ys);
        while yi > 0:
            print("new row")
            xi = 0;
            while cX < xs[-1]:
                print(30*"=")
                print("Getting", cX, cY)
                elevs, xa, ya = self.ds.getBlock(cY, cX) #in arguments are reversed....
                #plt.imshow(np.clip(elevs, 0, 10000))
                #plt.title("Loaded from srtm");
                #print data[0:len(rlon), 0:len(rlat)].shape#, elevs[rlon, rlat].shape
                print("Contains x values (long)", xa[0], xa[-1], "y values (lat)", ya[0], ya[-1])
                rx = self.resampleNearest(xs, xa)
                ry = self.resampleNearest(ys, ya)
                print("resampled x (lon)", rx)
                print("X-vals", xa[rx])
                print("resampled y (lat)", ry)
                print("Y-vals", ya[ry])
                resampledElevations = np.transpose(elevs[np.meshgrid(ry, rx)])
                print("resampled shape", resampledElevations.shape)
                #plt.figure()
                #plt.imshow(np.clip(resampledElevations, 0, 10000))
                #plt.title('Resampled elevations')
                #print "max amplitude raw", np.max(elevs), "resampled", np.max(resampledElevations)
                print("xi, y", xi, yi, "size", len(rx), len(ry))
                #sys.stdin.read(1)
                try:
                    print("X: got", len(rx), "samples, starting from ", xi)
                    print("Y: got", len(ry), "samples, starting from ", yi)
                    xind =list(range(xi, xi+len(rx)))
                    yind = list(range(yi-len(ry), yi))
                    print("X indexes", xind)
                    print("Y indexes", yind)
                    #arrgrid = np.array(np.meshgrid(yind, xind))
                    #print arrgrid
                    #print "print elevation data shape", resampledElevations.shape
                    resampledElevations = np.fliplr(resampledElevations)
                    data[np.meshgrid(xind, yind)] = resampledElevations;
                    #for i in range(len(xind)):
                    #    #print i
                    #    for j in range(len(yind)):
                    #        #try :
                    #            di = xind[i]
                    #            dj = yind[j]
                    #            #print di, dj, i, j
                    #            data[dj, di] = resampledElevations[j,i]
                    #        #except Exception as e:
                    #        #    print "Missed",(di, dj), (j, i)
                    #        #    print e
                    
                    #print "output destination shape", data[xind, yind]
                    #data[yind, xind]= resampledElevations
                except Exception as e:
                    import traceback
                    print("BEEEP", e)
                    traceback.print_exc()
                #print elevs[np.meshgrid(rlon, rlon)]
                #plt.imshow(np.fliplr(np.flipud(elevs)))
                #plt.imshow(np.clip(data, 0, 10000))
                #plt.figure();
                #plt.imshow(np.clip(data, 0, 10000))
                #plt.title('Appended to result');
                #plt.show()
                #print data[0:len(rlon), 0:len(rlat)].shape#, elevs[rlon, rlat].shape
                cX = xa[rx[-1]]
                xi += len(rx)
                #print "xi, yi", xi, yi
                #print "rlat", rlat, "rlon", rlon
            yi-=len(ry)
            cX = xs[0]
            cY = ys[-yi]
        print("Done getting data")
        return data;
 
    def getData2(self, xs, ys):
        import matplotlib.pyplot as plt
        #Ok unable to remember which is latitude and which is longitude.
        #x is longitude, and y is latitude. 
        print("x range is", xs[0], xs[-1], "yrange is", ys[0], ys[-1])
        data = np.zeros((xs.shape[0], ys.shape[0]))
        print("shape of destination is", data.shape)
        

        yToGet = ys
        yi = 0
        while len(yToGet) > 0:
            xi = 0
            xToGet = xs
            while len(xToGet) > 0:
                #print 30*"="
                #print "Remaining x samples", xToGet
                elevs, xa, ya = self.ds.getBlock(yToGet[0], xToGet[0])
                #print "Contains x values (long)", xa[0], xa[-1], "y values (lat)", ya[0], ya[-1]
                rx = self.resampleNearest(xToGet, xa)
                ry = self.resampleNearest(yToGet, ya)
                #print "resampled x (lon)", rx
                #print "X-vals", xa[rx]
                #print "resampled y (lat)", ry
                #print "Y-vals", ya[ry]
                resampledElevations = np.transpose(elevs[np.meshgrid(ry, rx)])
                #print "resampled shape", resampledElevations.shape
                xind =list(range(xi, xi+len(rx)))
                yind = list(range(yi, yi+len(ry)))
                #print "dest X indexes", xind
                #print "dest Y indexes", yind
                resampledElevations = np.flipud(np.fliplr(resampledElevations))
                data[np.meshgrid(xind, yind)] = resampledElevations;
                xToGet = xToGet[len(xind):]
                xi += len(xind)
            #print 40*'*'
            yToGet = yToGet[len(yind):]
            yi += len(yind)
        return data

        cX = xs[0]
        cY = ys[0]
        yi = len(ys);
        while yi > 0:
            print("new row")
            xi = 0;
            while cX < xs[-1]:
                print(30*"=")
                print("Getting", cX, cY)
                elevs, xa, ya = self.ds.getBlock(cY, cX) #in arguments are reversed....
                #plt.imshow(np.clip(elevs, 0, 10000))
                #plt.title("Loaded from srtm");
                #print data[0:len(rlon), 0:len(rlat)].shape#, elevs[rlon, rlat].shape
                print("Contains x values (long)", xa[0], xa[-1], "y values (lat)", ya[0], ya[-1])
                rx = self.resampleNearest(xs, xa)
                ry = self.resampleNearest(ys, ya)
                print("resampled x (lon)", rx)
                print("X-vals", xa[rx])
                print("resampled y (lat)", ry)
                print("Y-vals", ya[ry])
                resampledElevations = np.transpose(elevs[np.meshgrid(ry, rx)])
                print("resampled shape", resampledElevations.shape)
                #plt.figure()
                #plt.imshow(np.clip(resampledElevations, 0, 10000))
                #plt.title('Resampled elevations')
                #print "max amplitude raw", np.max(elevs), "resampled", np.max(resampledElevations)
                print("xi, y", xi, yi, "size", len(rx), len(ry))
                #sys.stdin.read(1)
                try:
                    print("X: got", len(rx), "samples, starting from ", xi)
                    print("Y: got", len(ry), "samples, starting from ", yi)
                    xind =list(range(xi, xi+len(rx)))
                    yind = list(range(yi-len(ry), yi))
                    print("X indexes", xind)
                    print("Y indexes", yind)
                    #arrgrid = np.array(np.meshgrid(yind, xind))
                    #print arrgrid
                    #print "print elevation data shape", resampledElevations.shape
                    resampledElevations = np.fliplr(resampledElevations)
                    data[np.meshgrid(xind, yind)] = resampledElevations;
                    #for i in range(len(xind)):
                    #    #print i
                    #    for j in range(len(yind)):
                    #        #try :
                    #            di = xind[i]
                    #            dj = yind[j]
                    #            #print di, dj, i, j
                    #            data[dj, di] = resampledElevations[j,i]
                    #        #except Exception as e:
                    #        #    print "Missed",(di, dj), (j, i)
                    #        #    print e
                    
                    #print "output destination shape", data[xind, yind]
                    #data[yind, xind]= resampledElevations
                except Exception as e:
                    import traceback
                    print("BEEEP", e)
                    traceback.print_exc()
                #print elevs[np.meshgrid(rlon, rlon)]
                #plt.imshow(np.fliplr(np.flipud(elevs)))
                #plt.imshow(np.clip(data, 0, 10000))
                #plt.figure();
                #plt.imshow(np.clip(data, 0, 10000))
                #plt.title('Appended to result');
                #plt.show()
                #print data[0:len(rlon), 0:len(rlat)].shape#, elevs[rlon, rlat].shape
                cX = xa[rx[-1]]
                xi += len(rx)
                #print "xi, yi", xi, yi
                #print "rlat", rlat, "rlon", rlon
            yi-=len(ry)
            cX = xs[0]
            cY = ys[-yi]
        print("Done getting data")
        return data;
 


num = 500
s = srtmManager()

em = ElevationDataManager(s)

###y = np.linspace(-60,-55,num)#+10+40
###x = np.linspace(8, 12, num)#+10
#lons = np.linspace(56,58, num)
#lats = np.linspace(11, 12, num)

#lons = np.linspace(10,13, num)
#lats = np.linspace(56, 58, int(num/3))

###data = em.getData2(x, y)
##data = np.fliplr(np.flipud(np.transpose(data)))
#elevs = np.ones((num,num))
#for x in range(num):
#    print "X", x
#    for y in range(num):
#        #print elevs.shape, lats.shape
#        elevs[x,y]=s.getElevation(lats[x], lons[y])
#elevs, lon, lat = s.getBlock(-12, 57)
#elevs = np.clip(elevs, 0, 3000)
###import matplotlib.pyplot as plt
#plt.imshow(np.fliplr(np.flipud(elevs)))
###plt.imshow(np.clip(data.T, 0, 10000), extent=[x[-1], x[1], y[0], y[1]])
###plt.show()
##print "test", s.getElevation(57.5,-13.5)
#s.buildIndex()
