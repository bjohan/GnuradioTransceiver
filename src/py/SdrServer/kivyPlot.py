'''
Mesh test
=========

This demonstrates the use of a mesh mode to distort an image. You should see
a line of buttons across the bottom of a canvas. Pressing them displays
the mesh, a small circle of points, with different mesh.mode settings.
'''
import numpy as np
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Mesh, Color
from functools import partial
from math import cos, sin, pi
import threading
import time


class PlotWidget(Widget):
    def __init__(self):
        self.xdata = np.array(range(10))
        self.ydata = np.array(range(10))
        super(PlotWidget, self).__init__()
        with self.canvas:
            self.mesh = self.build_mesh()

    def plot(self, idata):
        t0 = time.time()
        if len(idata.shape) > 1:
            data = idata[:,0]
        else:
            data = idata
        self.ydata = np.array(data);
        self.xdata = np.array(range(len(data)))
        self.canvas.clear()
        with self.canvas:
            Color(0,1.0,0)
            self.mesh = self.build_mesh()
        #print "Render rate", 1/(time.time()-t0)


    def build_mesh(self):
        """ returns a Mesh of a rough circle. """
        vertices = []
        indices = []
        width = self.size[0]
        height = self.size[1]
        minx = np.min(self.xdata)
        maxx = np.max(self.xdata)
        xr = maxx-minx;
        xs = float(width)/xr;
        miny = np.min(self.ydata)
        maxy = np.max(self.ydata)
        yr = maxy-miny;
        ys = float(height)/yr;
        t0 = time.time()
        zm = np.zeros(self.xdata.shape)
        v2 = np.vstack(((self.xdata-minx)*xs, (self.ydata-miny)*ys, zm, zm)).T
        indices = range(len(self.xdata))
        vertices = v2.ravel()
        return Mesh(vertices=vertices, indices=indices, mode='line_strip')
    


class MeshTestApp(App):
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
    #    print data
    #    self.y = data;
    #    self.x = range(len(data))
    #    #with self.widget.canvas:
    #    #    self.mesh = self.build_mesh()

    #def build_mesh(self):
    #    """ returns a Mesh of a rough circle. """
    #    vertices = []
    #    indices = []
    #    step = 10
    #    istep = (pi * 2) / float(step)
    #    for i in range(step): #range(len(self.x)):
    #        print self.y
    #        x = 300 + cos(istep * i) * 100+self.x[i]*10
    #        y = 300 + sin(istep * i) * 100+self.y[i]*10
    #        vertices.extend([x, y, 0, 0])
    #        indices.append(i)
    #    print "Updated plot"
    #    return Mesh(vertices=vertices, indices=indices)
    
    def build(self):
        self.wid = PlotWidget()
        print "build"
        #with wid.canvas:
        #    self.mesh = self.build_mesh()

        #layout = BoxLayout(size_hint=(1, None), height=50)
        #for mode in ('points', 'line_strip', 'line_loop', 'lines',
        #        'triangle_strip', 'triangle_fan'):
        #    button = Button(text=mode)
        #    button.bind(on_release=partial(self.change_mode, mode))
        #    layout.add_widget(button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(self.wid)
        #root.add_widget(layout)

        return root

def plot(vectors):
    pass
    global mta
    mta.plot(vectors)

mta = MeshTestApp()
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
