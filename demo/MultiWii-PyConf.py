import time
import threading
from pymultiwii import MultiWii
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.clock import Clock

serialPort = "/dev/tty.usbserial-AH01RI1Q"
board = MultiWii(serialPort)

class TextWidget(Widget):
	angXText = StringProperty()
	angYText = StringProperty()
	headingText = StringProperty()

	def __init__(self, **kwargs):
		super(TextWidget, self).__init__(**kwargs)
		event = Clock.schedule_interval(self.Update, 1 / 60.)

	def Update(self, dt):
		data = board.getData(MultiWii.ATTITUDE)
		if data == None:
			return
		self.angXText = "ang_x = " + str(data.get("angx"))
		self.angYText = "ang_y = " + str(data.get("angy"))
		self.headingText = "heading = " + str(data.get("heading"))

	def OnAccCalibrationButton(self):
		board.sendCMD(0, MultiWii.ACC_CALIBRATION, [])

	def OnMagCalibrationButton(self):
		board.sendCMD(0, MultiWii.MAG_CALIBRATION, [])


class PyConfApp(App):
	title = "MultiWii-PyConf"

	def build(self):
		root = TextWidget()
		return root

PyConfApp().run()
