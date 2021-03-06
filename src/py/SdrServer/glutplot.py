from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import openglplot
import sys
import time
import threading
import Queue
import numpy as np
name = 'ball_glut'
rot1 = 0.0
rot2 = 0.0

class PlotWindow:
    def __init__(self, w = 400, h=400, title="Plot", parent = None):
        self.stageLock = threading.Lock()
        self.staged = None
        self.parent = parent
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
        glutInitWindowSize(400,400)
        self.title=title
        self.window = glutCreateWindow(title)
        self.plotter = openglplot.PlotGl(w,h)
        glutDisplayFunc(self.display)
        glutCloseFunc(self.close)
        glutKeyboardFunc(self.keyboardFunc)
        self.paused = False
        self.active = True
        self.plotter.setupProjection()
        self.plotter.setData([0,1,2,3], [4,3,4,5])
     
    def isReady(self):
        return not self.stageLock.locked()

    def stageData(self, data):
        if self.stageLock.locked():
            #print "Dropping plot"
            return
        with self.stageLock:
            self.staged = data

    def plot(self, x = None, y = None):
        if self.active:
            self.stageData((x,y))

    def draw(self):
        self.plotter.draw()

    def presentData(self):
        doUpdate = False
        with self.stageLock:
            if self.staged is not None:
                if not self.paused:
                    self.plotter.setData(self.staged[0], self.staged[1])
                    doUpdate = True
                    self.staged = None
        #if doUpdate:
        #    self.update()
    
    def keyboardFunc(self, char, x,y):
        print self.title, char, x, y
        if char == 'p':
            self.paused = not self.paused

        if char == 's':
            self.plotter.autoScale = not self.plotter.autoScale

    def display(self):
        self.presentData()
        glClearColor(0.0,0.0,0.0,1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.plotter.setupProjection()
        self.plotter.draw()
        glutSwapBuffers()
        #glutPostRedisplay()

    def close(self):
        print "closing", self.title
        self.active = False
        self.parent.removePlot(self)


class PlotManager(threading.Thread):
    def __init__(self):
        #glutInit(sys.argv)
        self.cmdQ = Queue.Queue()
        self.plotQ = Queue.Queue()
        self.startLock = threading.Lock()
        self.startLock.acquire()
        self.windows = []
        self.currentWindow = 0
        threading.Thread.__init__(self)
        self.start()

    def finalize(self):
        #glutIdleFunc(self.idleFunc)
        self.start()

    def run(self):
        glutInit(sys.argv)

        #Wait for a plot window to be created befor entering glut main loop
        print "Waiting for first window"
        self.startLock.acquire()

        print "making first window"
        self.makeWindow()
        #self.windows.append(PlotWindow(title="SVEJS"))
        glutIdleFunc(self.idleFunc)
        glutMainLoop()

    def makeWindow(self):
        if not self.cmdQ.empty():
            cmd = self.cmdQ.get()
            if cmd[0] == 'create':
                self.windows.append(PlotWindow(title=cmd[1], parent = self))
                self.plotQ.put(self.windows[-1])
            if cmd[0] == 'remove':
                self.windows.remove(cmd[1])



    def idleFunc(self):
        self.makeWindow()
        #print "CW", self.currentWindow, len(self.windows),
        if self.currentWindow>=len(self.windows):
            self.currentWindow=0
        #print "CW", self.currentWindow, len(self.windows)
        if len(self.windows)>0:
            glutSetWindow(self.windows[self.currentWindow].window)
            glutPostRedisplay()
            self.currentWindow+=1
        else:
            glutLeaveMainLoop()

    def removePlot(self, target):
        self.cmdQ.put(('remove', target))


    def newPlot(self, title):
        self.cmdQ.put(('create', title))
        if self.startLock.locked():
            self.startLock.release()
        plt = self.plotQ.get()
        #self.windows.append(PlotWindow(title=title))
        #self.finalize()
        return plt

pm = PlotManager()

def Figure(title = "Figure"):
    return pm.newPlot(title)

def main():
    plots = []
    for i in range(5):
        plots.append(Figure("hej%d"%(i)))
    ndata = 2*8000;
    x = np.arange(ndata);
    t0 = time.time()
    while True:
        for p in plots: 
            y = np.sin(x/1000.0+time.time()-t0);
            p.plot(x,y)
        time.sleep(0.01)


if __name__ == '__main__': 
    main()
