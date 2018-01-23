import urllib2
import urllib
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
            print "downloading", url
            urllib.urlretrieve(url, self.getCacheName(url))
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
            print "Failed to load srtm index from", self.srtmIndex, "Downloading"
            self.buildIndex()
            self.srtms = self.scanIndex()
        if self.srtms is None:
            print "ERROR, failed to create SRTM index"
        else:
            print "SRTM index was successfully loaded"

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
        except Exception, e:
            print "Failed to build srtm", self.srtmIndex, e
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
        print "downloading", url
        r = urllib2.urlopen(url)
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

       
        L = 1201
        #Get name of the zip file containing data from cache.  
        if (int(lat), int(lon)) not in self.srtms:
            elevations = np.zeros((1201, 1201))
        else:
            url = self.srtms[(int(lat), int(lon))]
            cachename = self.cache.getUrl(url)
            zipname = os.path.basename(cachename)[:-4]

            #Open the zip file
            try:
                with zipfile.ZipFile(cachename) as f:
                    zipname = f.namelist()[0]
                    if f.namelist()[0]:
                        print "Loading", zipname
                        try:
                            with f.open(zipname) as hgt:
                                elevations = np.fromstring(hgt.read(), np.dtype('>i2', L*L)).reshape((L,L))
                        except Exception, e:
                            print "Error while parsing hgt from zip", hgt, zipname, e
                            elevations = np.zeros((1201, 1201))
                    else:
                        print zipname, "not in", f.namelist()
                        elevations = np.zeros((1201, 1201))
            except Exception, e:
                print "Error opening zip-file", cachename, e
        
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
                    #print "Loading", zipname
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
                    except Exception, e:
                        print "Error while parsing hgt from zip", hgt, zipname, e
                        elevations = np.zeros((1201, 1201))
                else:
                    print zipname, "not in", f.namelist()
                    elevations = np.zeros((1201, 1201))
        except Exception, e:
            print "Error opening zip-file", cachename, e
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
                
    def getData(self, lats, lons):
        data = np.zeros((lats.shape[0], lons.shape[0]))
        cLat = lats[0]
        cLon = lons[0]
        lati = len(lats);
        while lati > 0:
            loni = 0;
            while cLon < lons[-1]:
                #print "Getting", cLon, cLat
                elevs, lona, lata = self.ds.getBlock(cLat, cLon)
                rlat = self.resampleNearest(lats, lata)
                rlon = self.resampleNearest(lons, lona)
                resampledElevations = elevs[np.meshgrid(rlat, rlon)]
                print "max amplitude raw", np.max(elevs), "resampled", np.max(resampledElevations)
                print "Lat, lon", lati, loni, "size", len(rlat), len(rlon)
                sys.stdin.read(1)
                try:
                    arrgrid = np.meshgrid(range(lati-len(rlat), lati), range(loni, loni+len(rlon)))
                    print arrgrid
                    data[arrgrid]= elevs[np.meshgrid(rlat, rlon)]
                except:
                    print "BEEEP"
                #print elevs[np.meshgrid(rlon, rlon)]
                #print data[0:len(rlon), 0:len(rlat)].shape#, elevs[rlon, rlat].shape
                cLon = lona[rlon[-1]]
                loni += len(rlon)
                print lati, loni
                #print "rlat", rlat, "rlon", rlon
            lati-=len(rlat)
            cLon = lons[0]
            cLat = lata[rlat[-1]]
        print "Done getting data"
        return data;
 



num = 200
s = srtmManager()

em = ElevationDataManager(s)

#lats = np.linspace(-10,10,num)
#lons = np.linspace(-20, 30, num)
lons = np.linspace(109,112, num)
lats = np.linspace(50, 52, num)


data = em.getData(lats, lons)
#elevs = np.ones((num,num))
#for x in range(num):
#    print "X", x
#    for y in range(num):
#        #print elevs.shape, lats.shape
#        elevs[x,y]=s.getElevation(lats[x], lons[y])
#elevs, lon, lat = s.getBlock(-12, 57)
#elevs = np.clip(elevs, 0, 3000)
import matplotlib.pyplot as plt
#plt.imshow(np.fliplr(np.flipud(elevs)))
plt.imshow(np.clip(data, 0, 10000))
plt.show()
print "test", s.getElevation(57.5,-13.5)
#s.buildIndex()
