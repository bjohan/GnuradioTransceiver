import glfw
import OpenGL
import OpenGL.GL as gl
import openglplot
import time



class PlotWindow:
    def __init__(self):
        self.plotter = openglplot.PlotGl(640,480)
        self.window = glfw.create_window(640,480, "Plot", None, None)
        glfw.make_context_current(self.window)
        self.plotter.setupProjection()
        self.plotter.setData([0, 1, 2, 3], [0, 1, 0.2, 0.2])
        glfw.set_window_size_callback(self.window, self.resize_cb)
        
    def draw(self):
        self.plotter.draw()

    def resize_cb(self, window, w, h):
        self.plotter.width = w
        self.plotter.height = h
        self.plotter.setupProjection()
        self.update()


    def update(self):
        glfw.make_context_current(self.window)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.draw()
        glfw.swap_buffers(self.window)

def main():
    if not glfw.init():
        return

    pw = PlotWindow()
    # Loop until the user closes the window
    while not glfw.window_should_close(pw.window):
        #gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        #pw.draw()
        #glfw.swap_buffers(pw.window)
        pw.update()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

