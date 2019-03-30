import glfw
import OpenGL
import OpenGL.GL as gl
import openglplot
import time
import threading
import numpy as np
import prctl


class PlotWindow:
    def __init__(self, w = 640, h=480, title="Plot"):
        self.stageLock = threading.Lock()
        self.staged = None
        self.plotter = openglplot.PlotGl(w,h)
        self.window = glfw.create_window(w,h, title, None, None)
        glfw.make_context_current(self.window)
        self.plotter.setupProjection()
        self.plotter.setData([0,1,2,3], [4,3,4,5])
        glfw.set_window_size_callback(self.window, self.resize_cb)
        glfw.set_window_refresh_callback(self.window, self.refresh_cb)
      
    def stageData(self, data):
        with self.stageLock:
            self.staged = data
        glfw.post_empty_event()

    def plot(self, x = None, y = None):
        self.stageData((x,y))

    def draw(self):
        self.plotter.draw()

    def resize_cb(self, window, w, h):
        self.plotter.width = w
        self.plotter.height = h
        #self.plotter.setupProjection()


    def refresh_cb(self, window):
        self.update()

    def presentData(self):
        doUpdate = False
        with self.stageLock:
            if self.staged is not None:
                self.plotter.setData(self.staged[0], self.staged[1])
                doUpdate = True
                self.staged = None
        if doUpdate:
            self.update()
    
    def update(self):
        glfw.make_context_current(self.window)
        self.plotter.setupProjection()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.draw()
        glfw.swap_buffers(self.window)


class PlotManager(threading.Thread):
    def __init__(self, autoStart=True):
        glfw.init()
        threading.Thread.__init__(self)
        self.l = threading.Lock();
        self.windows = []
        if autoStart:
            self.start()

    def run(self):
        prctl.set_name("Plot rendering thread")
        while True:
            glfw.wait_events()
            glfw.poll_events()
            with self.l:
                for i in range(len(self.windows)):
                    if glfw.window_should_close(self.windows[i].window):
                        glfw.destroy_window(self.windows[i].window)
                        self.windows.pop(i)
                    else:
                        self.windows[i].presentData()

    def newPlot(self, title):
        with self.l:
            self.windows.append(PlotWindow(title=title))
            glfw.post_empty_event()
            return self.windows[-1]

pm = PlotManager()
def Figure(title="Plot"):
    return pm.newPlot(title)

#def main():  
#    figures = []
#    nplot = 3
#    for i in range(nplot):
#        figures.append(Figure( "Plot %d"%(i)))
#    while True:
#        time.sleep(2.0/30.0)
#        i = 0
#        for f in figures:
#            y = np.random.rand(100)+i
#            x = np.arange(100)
#            f.plot(x=x, y=y)
#            i+=1

#if __name__ == "__main__":
#    main()

