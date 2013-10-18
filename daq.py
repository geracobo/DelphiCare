#!/usr/bin/env python
# encoding utf-8

import time
import u3

class DAQ():
	"""
	DAQ class communicates with labjack.
	"""
	connected = False
	def __init__(self):
		try:
			self.daq = u3.U3()
			self.connected = True
		except:
			print "ERROR: No se pudo conectar con el DAQ."
			self.connected = False

