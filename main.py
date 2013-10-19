#!/usr/bin/env python
# coding=utf-8


import time
import thread
import threading
import multiprocessing
import random
import socket

SERVER_ADDRESS =  "162.243.55.207"
#SERVER_ADDRESS = "localhost"
SERVER_PORT = 8090

analog1 = 0
analog2 = 0


def main():
	print "Creando procesos de comunicación..."
	st = multiprocessing.Process(target=server_process)
	dt = multiprocessing.Process(target=daq_process)
	try:
		st.start()
		time.sleep(.5)
		dt.start()
	except:
		print "ERROR: No se pudieron crear los procesos de comunicación."

	cmd = ""
	while(cmd != "salir"):
		cmd = raw_input()
		parse_cmd(cmd)


	print "Terminando procesos..."
	st.terminate()
	dt.terminate()

def parse_cmd(cmd):
	if(cmd == ""):
		pass


def server_process():
	"""
	This thread communicates with the server.
	"""
	from server import Server
	print "Conectandose con el servidor..."
	try:
		server = socket.create_connection((SERVER_ADDRESS, SERVER_PORT))
	except:
		print "ERROR: No se pudo conectar con el servidor."
		return


	volts = 200
	delta = 0
	while True:
		print "Mandando", volts
		server.send(str(volts)+"\n")
		delta = random.randint(-1, 1)
		volts = volts + delta
		time.sleep(.01)

def daq_process():
	"""
	This thread communicates with the daq.
	"""

	from daq import DAQ
	print "Conectandose con el DAQ."
	daq = DAQ()

	if not daq.connected:
		return



	while True:
		pass

	#daq.setFIOState(4, state=1)
	#time.sleep(0.1)
	#analog1 = daq.getAIN(0)
	#daq.setFIOState(4, state=0)

	#time.sleep(0.1)

	#daq.setFIOState(5, state=1)
	#time.sleep(0.1)
	#analog2 = daq.getAIN(1)
	#daq.setFIOState(5, state=0)

	#time.sleep(0.1)



if __name__ == "__main__":
	main()

