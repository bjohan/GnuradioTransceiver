import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import os
import math
import zipfile
import numpy as np
import sys
from bs4 import BeautifulSoup

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

class SrtmData:
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
                    x = None
                    y = None
                    if 'W' in name:
                        #lon = int(name.split('W')[-1])
                        x = -int(name[4:7])
                    if 'E' in name:
                        #lon = 180-int(name.split('E')[-1])
                        x = int(name[4:7])
                    if 'N' in name:
                        y = int(name[1:3])
                    if 'S' in name:
                        y = -int(name[1:3])
                    #print x, y
                    index[(x, y)]= line
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

    def getBlock(self, x, y):
        """ get a datablock containing lat and lon"""

        x = int(x)
        y = int(y) 
        L = 1201
        #Get name of the zip file containing data from cache.  
        if (x,y) not in self.srtms:
            #print "E", x, "N", y, "is probably sea"
            elevations = np.zeros((1201, 1201))
        else:
            url = self.srtms[(x, y)]
            cachename = self.cache.getUrl(url)
            zipname = os.path.basename(cachename)[:-4]
            #print "Loading", zipname

            #Open the zip file
            try:
                with zipfile.ZipFile(cachename) as f:
                    zipname = f.namelist()[0]
                    if f.namelist()[0]:
                        #print "Loading", zipname
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
        
        xRange = np.linspace(x, x+1, L)
        yRange = np.linspace(y+1, y, L)
        
        return elevations, xRange, yRange
