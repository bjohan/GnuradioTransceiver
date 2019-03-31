import pyglet
import threading
import numpy as np
import time
import sys
class TraceData():
    #class to hold data for a plot trace
    def __init__(self, x=None, y=None):
        if x is None and y is None:
            raise ValueError("Both x and y  data cannot be None")

        if x is None:
            self.x = range(len(y))
        else:
            self.x = x

        if y is None:
            self.y = range(len(x))
        else:
            self.y = y

    def xSpan(self):
        return (np.min(self.x), np.max(self.x))

    def ySpan(self):
        return (np.min(self.y), np.max(self.y))

    def span(self):
        return(self.xSpan(), self.ySpan())
        
class Graticule:
    def __init__(self, mi, ma, numTicks = 7):
        self.scaleValues = np.array([1, 2, 5, 10])
        self.update(mi, ma, numTicks)

    def update(self, mi, ma, numTicks = 10):
        self.mi = mi
        self.ma = ma
        self.numTicks = numTicks
        self.ticks = self.compute()

    def computeTick(self):
        span = self.ma-self.mi
        if span == 0:
            span = 1
        ts = float(span)/float(self.numTicks)
        #print "span", span, "nt", self.numTicks, "ts", ts
        lv = np.floor(np.log10(ts))
        st = ts*10**(-lv)
        normTicks = self.scaleValues/st
        idx = (np.abs(np.log10(normTicks) - 0*1)).argmin()
        s = self.scaleValues[idx]
        sr = s*10**lv
        #print s, np.array([1,2,5,10]/ss)
        #print "min %0.3f\tmax %0.3f\tspan %0.3f\tts %0.3f\tlog10 tick%d\tlog10 %0.3f\tnorm %0.3f\ttickn %d  \ttick %0.3f"%(self.mi, self.ma, span, ts, lv,np.log10(span), st, s,sr)
        #print normTicks
        return sr    

    def compute(self):
        t = self.computeTick()
        nh = np.ceil(self.ma/t)
        nl = np.floor(self.mi/t)
        num = nh-nl
        #print "min/max", self.mi, self.ma, "tick", t, "low", nl*t, "high", nh*t, "num", num
        ticks = nl*t+np.array(range(int(num)+1))*t
        #for n in range(int(num)+1):
        #    print nl*t+n*t, 
        #print
        #print scale
        return ticks

class PlotWindow():
    def __init__(self, c, masterThread, title):
        self.masterThread = masterThread
        self.data = TraceData(np.random.rand(10))
        self.win = pyglet.window.Window(width = 400, height = 400, resizable=True, caption = title)
        self.win.on_show = self.on_show
        self.win.on_draw = self.on_draw
        self.win.on_resize = self.on_resize
        self.color =c

    def plot2(self, x, y):
        t0 = time.time()
        with self.masterThread.l:
            #print "Lock acq at", time.time()
            self.data = TraceData(x=x, y=y)
        print "put took", time.time()-t0
        print "trig at", time.time()
        self.masterThread.trigRedraw(self.win)
        

    def plot(self, idata):
        #print "Plot@", time.time()
        if len(idata.shape) > 1:
            data = idata[:,0]
        else:
            data = idata
 
        with self.masterThread.l:
            #print "Lock acq at", time.time()
            self.data = TraceData(x=data)
        self.masterThread.trigRedraw(self.win)


    def on_resize(self, width, height):
        print "Resize", width, height
        self.on_show()
        self.on_draw()

    def on_show(self):
        self.setupGl()


    def setupProjection(self):
        width = max(1, self.win.width)
        height = max(1, self.win.height)
        #print "Setting up projection for window of size", width, height
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(0, width, 0, height, -1000, 1000)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW) 

    def setupGl(self):
        pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
        self.setupProjection()
        # Set up projection matrix.
        #pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        #pyglet.gl.glLoadIdentity()
        #pyglet.gl.gluPerspective(45.0, float(self.win.width)/self.win.height, 0.1, 360)

    def on_draw(self):
        print "draw at", time.time()
        t0 = time.time()
        self.draw()
        print "draw took", time.time()-t0

    def dataToScreenCoords(self, x, y):
        xdata = np.array(x-self.xmin)*self.xs
        ydata = np.array(y-self.ymin)*self.ys
        return xdata, ydata

    def generateMeshAndIndices(self):
        vertices = []
        indices = []
        #xdata = np.array(self.data.x-self.xmin)*self.xs
        #ydata = np.array(self.data.y-self.ymin)*self.ys
        xdata, ydata = self.dataToScreenCoords(self.data.x, self.data.y)
        v2 = np.vstack(((xdata), (ydata))).T
        indices = range(len(xdata))
        vertices = v2.ravel()
        return (vertices, indices)

    def drawGraticule(self):
            vgl = Graticule(self.xmin, self.xmax)
            hgl = Graticule(self.ymin, self.ymax)
            v = []
            for l in vgl.ticks:
                x,y = self.dataToScreenCoords(l, 0)
                v+=[x, 0, x, self.win.height]
                l = pyglet.text.Label("%.2e"%l, x=x, y=0)
                l.draw()
            for l in hgl.ticks:
                x,y = self.dataToScreenCoords(0, l)
                v+=[0, y, self.win.width, y]
                l = pyglet.text.Label("%.2e"%l, x=0, y=y+2)
                l.draw()
            
            i = range(len(v)/2)
            print len(i)
            print len(v)
            pyglet.gl.glColor4f(0,1.0,0,1.0)
            pyglet.graphics.draw_indexed(len(i),pyglet.gl.GL_LINES, i, ('v2f', tuple(v)))



    def draw(self):
        self.win.clear()
        self.setupProjection()
        if self.data is not None:
            self.xmin, self.xmax  = self.data.xSpan()
            self.ymin, self.ymax  = self.data.ySpan()

            self.xs = self.win.width/(self.xmax-self.xmin)
            self.ys = self.win.height/(self.ymax-self.ymin)


            v, i = self.generateMeshAndIndices()
            self.drawGraticule()
            pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)
            pyglet.graphics.draw_indexed(len(i),pyglet.gl.GL_LINE_STRIP, i, ('v2f', tuple(v)))


            #l = pyglet.text.Label("hejsan", x=200, y=200)
            #l.draw()





class MyEventLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.l = threading.RLock()
        self.done = False

    def stop(self):
        with self.l:
            self.done = True

    def run(self):
        with self.l:
            pyglet.clock.tick()
            for window in pyglet.app.windows:
                window.dispatch_event('on_draw')
        while not self.done:
            #sys.stdout.write('.')
            #sys.stdout.flush()
            self.dispatchEvents()

    def trigRedraw(self, window):
        #print "Redraw trigged@", time.time()
        with self.l:
            window.switch_to()
            window.dispatch_event('on_draw')

    def dispatchEvents(self):
        t0 = time.time()
        with self.l:
            lt = time.time()-t0;
            if lt > 0.01:
                print "lock time", lt
            pyglet.clock.tick()
            for window in pyglet.app.windows:
                window.switch_to()
                window.dispatch_events()
                window.flip()

    def newPlot(self, arg, title):
        print "Creating new plot window"
        pw = None
        with self.l:
            pw = PlotWindow(arg, self, title)
            pw.win.dispatch_event('on_draw')
        return pw


el = MyEventLoop()
print el
print dir(el)
exit()
el.start()

#def Figure(arg, title):
#    global el
#    return el.newPlot(arg, title)

#tnum = 20
#np.random.seed(0)
#v1 = (np.random.rand(tnum)-0.5)*200
#v2 = (np.random.rand(tnum)-0.5)*200
#for i in range(tnum):
#    if v2[i] < v1[i]:
#        vmi = v2[i]
#        vma = v1[i]
#    else:
#        vmi = v1[i]
#        vma = v2[i]
#
#    g1 = Graticule(vmi, vma)
#    print vmi, vma, g1.ticks

#f1 = Figure(1.0, "ett")
#f2 = Figure(0.5, "b")
#f3 = Figure(0.0, "3")
#time.sleep(1)
#print "Plot to f1"
#f1.plot(np.random.rand(4)*10)
#f1.plot2([0,1,2], [0,1,0.2])
#f1.plot2(y=np.random.rand(10), x = np.arange(10))
#f1.plot(np.array(range(3)))
#time.sleep(3)
#print "plot to f2"
#f2.plot(np.random.rand(5))

#try:
#    while True:
#        f1.plot2(y=np.random.rand(10), x = np.arange(10))
#        f2.plot2(y=np.random.rand(10), x = np.arange(10))
#        time.sleep(0.001)
#except KeyboardInterrupt:
#    el.stop()

