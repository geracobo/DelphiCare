#!/usr/bin/env python
# encoding utf-8

import socketIO_client
import socket

class Server():
	def __init__(self, host, port=80):
		self.socket = socket.create_connection((host, port))

	def send_voltage(self, volts):
		self.socket.send(str(volts))