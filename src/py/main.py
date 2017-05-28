import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.config import Config
import encoder


class VfoScreen(GridLayout):
    def __init__(self, **kwargs):
        GridLayout.__init__(self,**kwargs)
        self.cols = 1
        self.f = 0
        self.vfoLabel = Label(text='Vfo Freq: 0Hz', font_size='40sp')
        self.add_widget(self.vfoLabel)
        self.add_widget(Button(text='select band'))
        print "Setting up thread"
        self.encoder = encoder.EncoderThread('/dev/serial0', self.updateFreq)

    def updateFreq(self, delta):
        self.f -= delta
        self.vfoLabel.text="VFO frequency %dHz"%(self.f)

    def stop(self):
        self.encoder.stop()

class MyApp(App):
    def build(self):
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '480')
        Config.set('graphics', 'fullscreen', '1')
        self.screen = VfoScreen()#Button(text='Hello World')
        #Clock.schedule_interval(self.update, 1)
        return self.screen

    def on_stop(self):
        self.screen.stop()
    #def update(self, *args):
    #    print  "Hejsan"
if __name__ == '__main__':
    MyApp().run()
