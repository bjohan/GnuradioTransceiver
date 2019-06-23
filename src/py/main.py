import kivy
kivy.require('1.0.8') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
#from mapwidget import MapWidget
#from af_widget import AfWidget
#from fftWidget import FftWidget
import encoder
import transceiverConfigWidget
from kivy.uix.textinput import TextInput

class VfoWidget(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self.f = 0

    def updateFreq(self, delta):
        self.f -= delta
        self.text="%dHz"%(self.f)

    def on_touch_down(self, touch):
        if touch.button == "scrolldown":
            self.updateFreq(1)
        if touch.button == "scrollup":
            self.updateFreq(-1)

class VfoScreen(GridLayout):
    def __init__(self, **kwargs):
        GridLayout.__init__(self,**kwargs)
        self.cols = 1
        self.f = 0
        self.vfoLabel = VfoWidget(text='0Hz', font_size='40sp', size_hint=(1.0, 0.2))

	self.tabs = TabbedPanel(size_hint=(1.0, 0.8))	
	self.tabs.default_tab_text = 'XCVR CFG'
	self.tabs.default_tab_content = transceiverConfigWidget.TransceiverConfigWidget()#Label(text="rtx")

        #self.afTab = TabbedPanelHeader(text="AF")
        #self.afTab.content = AfWidget() #Label(text="AF control");
        #self.tabs.add_widget(self.afTab)

	#self.modTab = TabbedPanelHeader(text='Modulation')
	#self.modTab.content = Label(text="Select modulation")
	#self.tabs.add_widget(self.modTab)

	#self.rotorTab = TabbedPanelHeader(text='Rotor control')
	#self.tabs.add_widget(self.rotorTab)
	#self.rotorTab.content = Label(text="ROTOR");

	#self.statusTab = TabbedPanelHeader(text='Status')
	#self.tabs.add_widget(self.statusTab)
	#self.statusTab.content = Label(text="STATUS");

	#self.fftTab = TabbedPanelHeader(text='FFT')
	#self.tabs.add_widget(self.fftTab)
	#self.fftTab.content = FftWidget() # Label(text="FFT");

	#self.mapTab = TabbedPanelHeader(text="Map")
	#self.tabs.add_widget(self.mapTab)
	#self.mapTab.content = MapWidget()


	self.add_widget(self.tabs)
        self.add_widget(self.vfoLabel)
        print "Setting up thread"
        self.encoder = encoder.EncoderThread('/dev/serial0', self.updateFreq)

    def updateFreq(self, delta):
        self.vfoLabel.updateFreq(delta)
        #self.f -= delta
        #self.vfoLabel.text="%dHz"%(self.f)

    def stop(self):
        self.encoder.stop()

class MyApp(App):
    title = "SDR transceiver"
    def build(self):
        #Config.set('graphics', 'width', '800')
        #Config.set('graphics', 'height', '480')
	#Window.size=(800, 480)
	#Window.fullscreen = True
        Config.set('graphics', 'fullscreen', 'auto')
        self.screen = VfoScreen()#Button(text='Hello World')
        #Clock.schedule_interval(self.update, 1)
        return self.screen

    def on_stop(self):
        self.screen.stop()
    #def update(self, *args):
    #    print  "Hejsan"
if __name__ == '__main__':
    MyApp().run()
