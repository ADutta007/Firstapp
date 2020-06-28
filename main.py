import kivy
from kivy.app import App
from kivy.uix.label import Label
class Myapp(App):
	def build(self):
		return Label(text="Ashish__Ameet")
if __name__=="__main__":
	Myapp().run()
