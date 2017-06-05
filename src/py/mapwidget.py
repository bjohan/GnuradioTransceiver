from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, UpdateNormalMatrix, Mesh
from kivy.graphics.opengl import *
from kivy.graphics.instructions import RenderContext, Callback
from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Translate, Rotate
from kivy.clock import Clock
from kivy.graphics.transformation import Matrix
#from objloader import ObjFile
from kivy.resources import resource_find
import random
import numpy as np



class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        #self.scene = ObjFile(resource_find("monkey.obj"))
        super(Renderer, self).__init__(**kwargs)
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.canvas['projection_mat'] = proj
        self.canvas['diffuse_light'] = (0.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (0.1, 0.6, 0.1)
        #self.rot.angle += 1

    def on_touch_move(self,  t):
        self.rot.angle += t.dx
        self.rotx.angle -= t.dy
        #print t.dx

    def generateHeightData(self, sx, sy, za):
        return np.random.rand(sx, sy)*za

    def calcNormals(self, hgt):
        normals = np.ones((hgt.shape[0], hgt.shape[1], 3))
        sx = hgt.shape[0]
        sy = hgt.shape[1]
        for x in range(sx):
            for y in range(sy):
                if x < sx-1:
                    xp1 = hgt[x+1,y]
                else:
                    xp1 = hgt[sx-1, y]
                
                if y < sy-1:
                    yp1 = hgt[x,y+1]
                else:
                    yp1 = hgt[x, sy-1]
                p = hgt[x,y]
                vxp1 = np.array([x+1, y, xp1])
                vyp1 = np.array([x, y+1, yp1])
                v = np.array([x, y, p])
                normal = np.cross(vxp1-v, vyp1-v)
                normal = normal/abs(normal)
                normals[x, y, :] = normal
        return normals; 

    def generateTriangleCounterClockWiseIndices(self, hgt):
        sx, sy = hgt.shape
        idcl = np.arange(sx*sy) 
        print "IDCL", idcl.shape, sx, sy
        idcs = np.reshape(idcl, (sx, sy))
        print "Data shape", hgt.shape, "index shape", idcs.shape
        idc = []
        for x in range(sx-1):
            for y in range(sy-1):
                #Upper triangle
                idc.extend([idcs[x, y+1], idcs[x+1, y], idcs[x, y]])
                #Lower triangle
                idc.extend([idcs[x, y+1], idcs[x+1, y+1], idcs[x+1, y]])
        return idc
                

    def generateMesh(self):
        hgt = self.generateHeightData(100, 100, 0.1);
        norm = self.calcNormals(hgt)
        idcs = self.generateTriangleCounterClockWiseIndices(hgt)
        print hgt.shape
        vtx = []
        idx = []
        i = 0;
        for x in range(hgt.shape[0]):
            for y in range(hgt.shape[1]):
                vtx.extend( [float(x)/10.0-5,  hgt[x,y], float(y)/10.0-5, 
                        norm[x, y, 0]/10.0, norm[x, y, 1], norm[x, y, 2]/10.0, 
                        0.0,        0.0,    ])
                idx.append(i)
                i+=1
        m= Mesh(vertices = vtx, indices = idcs, mode='triangles', fmt=[('v_pos', 3, 'float'), ('v_normal', 3, 'float'), ('v_tc0', 2, 'float')])#[(b'v_pos', 2, b'float'), (b'tc', 2, b'float')])
        return m

    def setup_scene(self):
        Color(1, 0, 1, 1)
        PushMatrix()
        Translate(0, -3, -10)
        self.rotx = Rotate(0, 1, 0, 0);
        self.rot = Rotate(0.5, 0, 1, 0)
        #m = random.sample(xrange(10), 10)#list(self.scene.objects.values())[0]
        #m = list(self.scene.objects.values())[0]
        self.mesh = self.generateMesh()#Mesh(
        UpdateNormalMatrix()
        #self.mesh = Mesh(
        #    vertices=m.vertices,
        #    indices=m.indices,
        #    fmt=m.vertex_format,
        #    mode='triangles',
        #)
        PopMatrix()




class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        print "size", self.width, self.height, "pos", touch.x, touch.y
        if touch.x < self.width+self.x and touch.y < self.height+self.y:
            #with self.canvas:
                Color(1, 1, 0)
                d = 30.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))




class MapWidget(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        self.cols = 1
        GridLayout.__init__(self, **kwargs)
        topLayout=BoxLayout(orientation = "vertical")
        topLayout.add_widget(Button(text="first", size_hint=(1.0, 0.1)))
        topLayout.add_widget(Renderer(size_hint=(1.0, 0.8)))
        topLayout.add_widget(Button(text="second", size_hint=(1.0,0.1)))
        self.add_widget(topLayout)
