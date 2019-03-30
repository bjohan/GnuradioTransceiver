import OpenGL.GL as gl
import OpenGL.GLUT as glut
import numpy as np
import ctypes
import time

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
        lv = np.floor(np.log10(ts))
        st = ts*10**(-lv)
        normTicks = self.scaleValues/st
        idx = (np.abs(np.log10(normTicks) - 0*1)).argmin()
        s = self.scaleValues[idx]
        sr = s*10**lv
        return sr    

    def compute(self):
        t = self.computeTick()
        nh = np.ceil(self.ma/t)
        nl = np.floor(self.mi/t)
        num = nh-nl
        ticks = nl*t+np.array(range(int(num)+1))*t
        return ticks

class PlotGl():
    #Class that draws plots using opengl
    def __init__(self, w,h):
        glut.glutInit()
        self.width = w
        self.height = h
        self.color = (0,1,0)

    def setData(self, x, y):
        self.data = TraceData(x=x, y=y)

    def setTrace(self, t):
        self.data = t

    def setupProjection(self):
        width = max(1, self.width)
        height = max(1, self.height)
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1000, 1000)
        gl.glMatrixMode(gl.GL_MODELVIEW) 

    def setupGl(self):
        gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
        self.setupProjection()

    def dataToScreenCoords(self, x, y):
        xdata = np.array(x-self.xmin)*self.xs
        ydata = np.array(y-self.ymin)*self.ys
        return xdata, ydata

    def generateMeshAndIndices(self):
        vertices = []
        indices = []
        xdata, ydata = self.dataToScreenCoords(self.data.x, self.data.y)
        v2 = np.vstack(((xdata), (ydata))).T
        indices = range(len(xdata))
        vertices = v2.ravel()
        return (vertices, indices)

    def drawLabel(self, text, x,  y,  font=glut.GLUT_BITMAP_9_BY_15,  c = [1.0,1.0,1.0]):
        gl.glRasterPos2f(int(x),int(y))
        glut.glutBitmapString(font, text)
        #for c in text:
        #    glut.glutBitmapCharacter( font , ctypes.c_int( ord(c) ) )


    def drawGraticule(self):
            vgl = Graticule(self.xmin, self.xmax)
            hgl = Graticule(self.ymin, self.ymax)
            v = []
            for l in vgl.ticks:
                x,y = self.dataToScreenCoords(l, 0)
                v+=[x, 0, x, self.height]
                self.drawLabel( "%.2e"%l, x+2 , y+2)
            for l in hgl.ticks:
                x,y = self.dataToScreenCoords(0, l)
                v+=[0, y, self.width, y]
                self.drawLabel( "%.2e"%l, x+2 , y+2)
            
            gl.glColor4f(0,1.0,0,1.0)
            gl.glBegin(gl.GL_LINES)
            for i in range(len(v)/2):
                gl.glVertex2fv(v[2*i:2*i+2])
            gl.glEnd()



    def draw(self):
        if self.data is not None:
            t0 = time.time();
            self.xmin, self.xmax  = self.data.xSpan()
            self.ymin, self.ymax  = self.data.ySpan()
            if self.xmax == self.xmin:
                self.xs = 1.0
            else:
                self.xs = self.width/(self.xmax-self.xmin)
            if self.ymax == self.ymin:
                self.ys = 1.0
            else:
                self.ys = self.height/(self.ymax-self.ymin)
            #print self.width, self.height

            t0 = time.time()
            v, i = self.generateMeshAndIndices()
            self.drawGraticule()
            gl.glColor4f(1.0,1.0,1.0,1.0)
            gl.glBegin(gl.GL_LINE_STRIP)
            for i in range(len(v)/2):
                gl.glVertex2fv(v[2*i:2*i+2])
            gl.glEnd()
            fps = 1.0/(time.time()-t0)
            self.drawLabel("FPS %0.2f"%(fps), self.width-100,self.height-20)
            #print "gl trace", time.time()-t0

