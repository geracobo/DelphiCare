#!/usr/bin/env python
# encoding utf-8

import time
import u3

class DAQ():
	def __init__(self):
		try:
			self.daq = u3.U3()
		except:
			print "Error al conectarse al DAQ."

