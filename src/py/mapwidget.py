from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse

class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        with self.canvas:
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
		topLayout.add_widget(MyPaintWidget(size_hint=(1.0, 0.8)))
        	topLayout.add_widget(Button(text="second", size_hint=(1.0,0.1)))
        	self.add_widget(topLayout)
