import serial
import threading
import Queue
import time

class EncoderThread(threading.Thread):
	def __init__(self, port, callback = None):
		threading.Thread.__init__(self)
		self.q = Queue.Queue()
		self.s = serial.Serial(port, 9600)
		self.start()
		self.callback = callback
		self.last = None

	def run(self):
		while True:
			val = int(self.s.readline())
			if self.last is None:
				self.last = val
			
			delta = val - self.last
		

			if abs(delta) > 32768:
				if self.last < 32768:
					delta = self.last+65536-val	
				else:
					delta = 65536-self.last+val
			self.last = val

			if self.callback is not None and delta != 0:
				self.callback(delta)
	
			if not self.q.empty():
				c = self.q.get()
				if c == 'stop':
					break

	def stop(self):
		self.q.put('stop')

#def cb(delta):
#	print delta

#e = EncoderThread('/dev/serial0', cb)
#time.sleep(5)
#e.stop()
