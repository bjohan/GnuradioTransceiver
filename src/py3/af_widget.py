from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.button import Button

from pyaudio import PyAudio


class AfInputDevice(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        self.cols = 1
        GridLayout.__init__(self, **kwargs)
        self.topLayout=BoxLayout(orientation = "vertical")
        self.add_widget(self.topLayout)
        self.topLayout.add_widget(Label(text='tjosan'))

class AfInputManager(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 2
        self.cols = 1
        GridLayout.__init__(self, **kwargs)

        self.mainPanel = TabbedPanel()
        self.mainPanel.default_tab_content = AfInputDevice()
        print("WIDTH", self.width)
        self.mainPanel.default_tab_text = "Default Input"
        self.add_widget(self.mainPanel)
        self.add_widget(Button(text="Add new"))



class AfWidget(GridLayout):
    def __init__(self, **kwargs):
        self.p = PyAudio()
        self.rows = 1
        self.cols = 1
        GridLayout.__init__(self, **kwargs)

        self.mainPanel = TabbedPanel()
        print("WIDTH", self.width)
        self.mainPanel.default_tab_text = "AF Output Devices"

        self.add_widget(self.mainPanel)
        self.inputPanel = TabbedPanelHeader(text="AF Input Devices")
        self.inputPanel.content = AfInputManager()
        self.mainPanel.add_widget(self.inputPanel)
        self.mainPanel.tab_width = 200
        #topLayout = BoxLayout(orientation = "vertical")
        
        #topLayout.add_widget(Label(text="Input device", ))
        #self.inputDevs = Spinner(text = "Select input")
        #topLayout.add_widget(self.inputDevs)
        
        #topLayout.add_widget(Label(text="Output device", ))
        #self.outputDevs = Spinner(text = "Select output")
        #topLayout.add_widget(self.outputDevs)
        
        #self.updateSoundDevices()
        #self.add_widget(topLayout)

    def updateSoundDevices(self):
        api_cnt = self.p.get_host_api_count()
        dev_cnt = self.p.get_device_count()
        inputs = []
        outputs = []
        print("Number of API's", api_cnt, "Number of sound devices", dev_cnt)
        for i in range(dev_cnt):
            d = self.p.get_device_info_by_index(i)
            if d['maxInputChannels'] > 0:
                inputs.append(d['name'])
            if d['maxOutputChannels'] > 0:
                outputs.append(d['name'])

        print("inputs", inputs)
        print("outputs", outputs)
        self.inputDevs.values = inputs
        self.outputDevs.values = outputs


