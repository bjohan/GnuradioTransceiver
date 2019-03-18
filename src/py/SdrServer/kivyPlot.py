'''
Mesh test
=========

This demonstrates the use of a mesh mode to distort an image. You should see
a line of buttons across the bottom of a canvas. Pressing them displays
the mesh, a small circle of points, with different mesh.mode settings.
'''
import os
#os.environ["KIVY_NO_CONSOLELOG"] = "1"
import numpy as np
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Mesh, Color, Rectangle
from kivy.core.text import Label as CoreLabel
from functools import partial
from math import cos, sin, pi
import threading
import time

class PlotWidget(Widget):
    def __init__(self):
        self.xdata = np.array(range(10))
        self.ydata = np.array(range(10))
        self.lock = threading.Lock()
        super(PlotWidget, self).__init__()
        self.register_event_type('on_update_plot')
        self.on_update_plot()
        #with self.canvas:
        #    self.mesh = self.build_mesh()

    def on_update_plot(self):
        self.width = self.size[0]
        self.height = self.size[1]
        self.minx = np.min(self.xdata)
        self.maxx = np.max(self.xdata)
        self.xr = self.maxx-self.minx;
        self.xs = float(self.width)/self.xr;
        self.miny = np.min(self.ydata)
        self.maxy = np.max(self.ydata)
        self.yr = self.maxy-self.miny;
        self.ys = float(self.height)/self.yr;
        self.drawMesh()

    def drawText(self, pos, text, font_size = 12):
        l = CoreLabel(text=text, font_size = font_size)
        l.refresh()
        Rectangle(pos=pos, size=l.size, texture=l.texture)

    def drawGraticule(self, lines = 10):
        hLines = np.linspace(0,self.height, lines)
        vLines = np.linspace(0,self.width,lines)
        vs = self.computeScaleLines(self.minx, self.maxx, lines)
        hs = self.computeScaleLines(self.miny, self.maxy, lines)

        with self.canvas:
            Color(1.00,0.0,0)
            self.mesh = self.buildGraticule(hLines, vLines)
        with self.canvas:
            Color(1.0,1.0,1.0)
            self.drawGraticuleText(hLines, vLines, hs, vs)

    def computeScaleLines(self, mi, ma, num):
        return np.linspace(mi, ma, num)

    def drawGraticuleText(self, hlines, vlines, hvalues, vvalues, font_size = 12):
        hci = np.round(len(hlines)/2)
        vci = np.round(len(vlines)/2)
        for (v, i) in zip(vlines, vvalues):
            self.drawText((v,hlines[hci]-font_size-1), "%.3e"%(i), font_size = font_size)
        for (h, i) in zip(hlines, hvalues):
            self.drawText((vlines[vci],h), "%.3e"%(i), font_size = font_size)

    def buildGraticule(self, hlines, vlines):
        vt = []
        indices = []
        for h in hlines:
            vt.extend([0,h, 0,0, self.width, h,0,0])

        for v in vlines:
            vt.extend([v, 0, 0,0, v, self.height,0,0])
        indices.extend(range(len(vt)/4))


        return Mesh(vertices=vt, indices=indices, mode='lines')

    def drawMesh(self):
        self.canvas.clear()
        self.drawGraticule()
        with self.canvas:
            Color(0,1.0,0)
            self.mesh = self.build_mesh()

    def plot(self, idata):
        if self.lock.locked():
            return
        with self.lock:
            t0 = time.time()
            if len(idata.shape) > 1:
                data = idata[:,0]
            else:
                data = idata
            self.ydata = np.array(data);
            self.xdata = np.array(range(len(data)))
        #self.drawMesh()
        self.dispatch('on_update_plot')
        #print "Render rate", 1/(time.time()-t0)
    

    def build_mesh(self):
        with self.lock:
            vertices = []
            indices = []
            t0 = time.time()
            zm = np.zeros(self.xdata.shape)
            v2 = np.vstack(((self.xdata-self.minx)*self.xs, (self.ydata-self.miny)*self.ys, zm, zm)).T
            indices = range(len(self.xdata))
            vertices = v2.ravel()
        return Mesh(vertices=vertices, indices=indices, mode='line_strip')
    


class KivyPlotApp(App):
    def __init__(self):
        self.x = range(10)
        self.y = range(10)
        self.wid = None
        App.__init__(self)


    def change_mode(self, mode, *largs):
        self.mesh.mode = mode

    def plot(self, data):
        if self.wid is not None:
            self.wid.plot(data)
    
    def build(self):
        self.wid = PlotWidget()
        print "build"
        root = BoxLayout(orientation='vertical')
        root.add_widget(self.wid)

        return root

def plot(vectors):
    pass
    global mta
    mta.plot(vectors)

mta = KivyPlotApp()
def launch():
    global mta
    #mta = MeshTestApp()
    mta.run()

def stop():
    global mta
    mta.stop()
print "Starting plot Thread"
plotThread = threading.Thread(target = launch, name = "kivy_plot")
plotThread.start()
print "Plot thread running"

def join():
    print "Waiting for plot threa to join"
    plotThread.join()

#if __name__ == '__main__':
#    MeshTestApp().run()
