from math import *
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
	accXText = StringProperty()
	accYText = StringProperty()
	accZText = StringProperty()

	gyrXText = StringProperty()
	gyrYText = StringProperty()
	gyrZText = StringProperty()

	magXText = StringProperty()
	magYText = StringProperty()
	magZText = StringProperty()

	angXText = StringProperty()
	angYText = StringProperty()
	headingText = StringProperty()

	def __init__(self, **kwargs):
		super(TextWidget, self).__init__(**kwargs)
		event = Clock.schedule_interval(self.Update, 1 / 60.)

	def Update(self, dt):
		data = board.getData(MultiWii.RAW_IMU)
		if data == None:
			return

		self.accXText = str(data.get("ax"))
		self.accYText = str(data.get("ay"))
		self.accZText = str(data.get("az"))

		self.gyrXText = str(data.get("gx"))
		self.gyrYText = str(data.get("gy"))
		self.gyrZText = str(data.get("gz"))

		self.magXText = str(data.get("mx"))
		self.magYText = str(data.get("my"))
		self.magZText = str(data.get("mz"))

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

	def OnArmButton(self):
		board.arm()

	def OnDisarmButton(self):
		board.disarm()


class PyConfApp(App):
	title = "MultiWii-PyConf"

	def build(self):
		root = TextWidget()
		return root

PyConfApp().run()
