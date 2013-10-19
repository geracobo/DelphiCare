#!/usr/bin/env python
# encoding utf-8

import socket

class Server():
	"""
	Server class communicates with nodejs through tcp.
	"""
	connected = False
	def __init__(self, host, port=80):
		try:
			self.sock = socket.create_connection((host, port))
			self.connected = True
			print "Servidor conectado."
		except:
			print "ERROR: No se pudo conectar al servidor."
			self.connected = False

	def send_voltage(self, volts):
		self.sock.send(str(volts))