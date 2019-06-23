from kivy.core.window import Window
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, UpdateNormalMatrix, Mesh
from kivy.graphics.opengl import *
from kivy.graphics.instructions import RenderContext, Callback
from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Translate, Rotate, Scale
from kivy.clock import Clock
from kivy.graphics.transformation import Matrix
#from objloader import ObjFile
from kivy.resources import resource_find

import SdrServer.soapySdrDevice

class LabeledInput(BoxLayout):
    def __init__(self, label = "Label", default = "Default", orientation = "horizontal"):
        BoxLayout.__init__(self, orientation = orientation)
        self.add_widget(Label(text=label))
        Window.release_all_keyboards()
        self.add_widget(TextInput(text = default, multiline=False))

class TransceiverConfigWidget(BoxLayout):
    def __init__(self, **kwargs):
        #self.rows = 10
        #self.cols = 1
        BoxLayout.__init__(self, orientation="vertical", **kwargs)
        self.d = SdrServer.soapySdrDevice.SoapySdrManager()
        self.deviceLabels = []
        for d in self.d.getSdrs():
            self.deviceLabels.append(d.getItems()['label'])
        self.rxSpinner = Spinner(text = 'RX device', values = self.deviceLabels);
        self.txSpinner = Spinner(text = 'TX device', values = self.deviceLabels);
        #topLayout=BoxLayout(orientation = "vertical")
        #midLayout = BoxLayout(orientation = "horizontal", size_hint=(1.0,0.8))
        #swLayout = BoxLayout(orientation = "vertical", size_hint=(0.2, 1.0))
        #swLayout.add_widget(Label(text="Zoom"))
        #self.zs = Switch()
        #self.zs.bind(active=self.zoomSwitchLogic)
        #swLayout.add_widget(self.zs)
        #swLayout.add_widget(Label(text="Pan"))
        #self.ps = Switch()
        #self.ps.bind(active=self.panSwitchLogic)
        #swLayout.add_widget(self.ps)
        #midLayout.add_widget(Renderer(self.zs, self.ps, size_hint=(0.8, 1.0)))
        #midLayout.add_widget(swLayout)
       
       # topLayout.add_widget(Button(text="first", size_hint=(1.0, 0.1)))
       # #topLayout.add_widget(Renderer(size_hint=(1.0, 0.8)))
        #topLayout.add_widget(midLayout)
        #topLayout.add_widget(Button(text="second", size_hint=(1.0,0.1)))
        #self.add_widget(Label(text="hejsan"))
        self.add_widget(Label(text='Configure transceiver properties'))
        self.add_widget(self.txSpinner)
        self.txLoOffs=LabeledInput(label="TX LO offs", default="0")
        self.add_widget(self.txLoOffs)
        self.add_widget(self.rxSpinner)
        self.rxLoOffs=LabeledInput(label="RX LO offs", default="0")
        self.add_widget(self.rxLoOffs)
        #self.add_widget(TextInput(text="hej"))

