from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import openglplot
import sys
import time
import threading
import queue
import numpy as np
name = 'ball_glut'
rot1 = 0.0
rot2 = 0.0

class PlotWindow:
    def __init__(self, w = 400, h=400, title="Plot", parent = None):
        self.stageLock = threading.Lock()
        self.staged = None
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
        glutInitWindowSize(400,400)
        self.window = glutCreateWindow(title)
        self.plotter = openglplot.PlotGl(w,h)
        glutDisplayFunc(self.display)
        self.plotter.setupProjection()
        self.plotter.setData([0,1,2,3], [4,3,4,5])
     
    def isReady(self):
        return not self.stageLock.locked()

    def stageData(self, data):
        if self.stageLock.locked():
            print "Dropping plot"
            return
        with self.stageLock:
            self.staged = data

    def plot(self, x = None, y = None):
        self.stageData((x,y))

    def draw(self):
        self.plotter.draw()

    def presentData(self):
        doUpdate = False
        with self.stageLock:
            if self.staged is not None:
                self.plotter.setData(self.staged[0], self.staged[1])
                doUpdate = True
                self.staged = None
        #if doUpdate:
        #    self.update()
    
    def display(self):
        self.presentData()
        glClearColor(0.0,0.0,0.0,1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.plotter.setupProjection()
        self.plotter.draw()
        glutSwapBuffers()
        #glutPostRedisplay()

    def close(self):
        self.parent.close(self)


class PlotManager(threading.Thread):
    def __init__(self):
        #glutInit(sys.argv)
        self.cmdQ = queue.Queue()
        self.plotQ = queue.Queue()
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
                self.windows.append(PlotWindow(title=cmd[1]))
                self.plotQ.put(self.windows[-1])

    def idleFunc(self):
        self.makeWindow()
        print "CW", self.currentWindow, len(self.windows),
        if self.currentWindow>=len(self.windows):
            self.currentWindow=0
        print "CW", self.currentWindow, len(self.windows)
        glutSetWindow(self.windows[self.currentWindow].window)
        glutPostRedisplay()
        self.currentWindow+=1

    def newPlot(self, title):
        self.cmdQ.put(('create', title))
        if self.startLock.locked():
            self.startLock.release()
        plt = self.plotQ.get()
        #self.windows.append(PlotWindow(title=title))
        #self.finalize()
        return plt


pltr = openglplot.PlotGl(400,400)
pltr.setData([0,1,2,3], [4,3,4,5])

def main():
    pm = PlotManager()
    #pm.start()
    plots = []
    for i in range(5):
        plots.append(pm.newPlot("hej%d"%(i)))
    ndata = 400;
    x = np.arange(ndata);
    t0 = time.time()
    while True:
        for p in plots: 
            y = np.sin(x/10.0+time.time()-t0);
            p.plot(x,y)
    #time.sleep(3)
    #glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    #glutInitWindowSize(400,400)
    #glutCreateWindow("BRAPP")
    #glutDisplayFunc(display1)
    #glutInit(sys.argv)
    #glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    #glutInitWindowSize(400,400)
    #glutCreateWindow("BRAPP")
    #glutDisplayFunc(display1)
    #pw = PlotWindow()
    #glutMainLoop()

def display1():
    global rot1
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    pltr.setupProjection()
    pltr.draw()
    glutSwapBuffers()
    #glutPostRedisplay()


if __name__ == '__main__': 
    main()
