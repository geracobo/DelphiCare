#!/usr/bin/env python
# coding=utf-8


import time
import multiprocessing

SERVER_ADDRESS =  "162.243.55.207"
#SERVER_ADDRESS = "localhost"
SERVER_PORT = 8090




def main():
	"""
	Main Process.
	"""

	ekg_queue = multiprocessing.Queue()
	spo2_queue = multiprocessing.Queue()

	print "Creando procesos de comunicación..."
	st = multiprocessing.Process(target=server_process, args=(ekg_queue, spo2_queue))
	dt = multiprocessing.Process(target=daq_process, args=(ekg_queue, spo2_queue))

	st.daemon = True
	dt.daemon = True

	try:
		st.start()
		time.sleep(1)
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


def server_process(ekg_queue, spo2_queue):
	"""
	This thread communicates with the server. When it finds data in the
	queue, it creates a packet with the following form:

	{
		ekg: ekg_value,
		spo2: spo2_value
	}

	"""
	import socket
	import json

	print "Conectandose con el servidor..."
	try:
		server = socket.create_connection((SERVER_ADDRESS, SERVER_PORT), timeout=.5)
	except:
		print "ERROR: No se pudo conectar con el servidor."
		return


	while True:
		packet= {}
		if not ekg_queue.empty():
			packet['ekg'] = ekg_queue.get()
		if not spo2_queue.empty():
			packet['spo2'] = spo2_queue.get()

		packetJson = json.dumps(packet)

		print "Mandando Paquete: ", packetJson
		server.send(str(packetJson)+"|")
		time.sleep(.01)

def daq_process(ekg_queue, spo2_queue):
	"""
	This thread communicates with the daq.
	"""

	import random

	#volts = 200
	#delta = 0
	#while True:
	#	delta = random.randint(-5,5)
	#	volts = volts + delta
	#	ekg_queue.put(volts)
	#	spo2_queue.put(5)

	from u3 import U3
	from math import log, fabs, log10

	print "Conectandose con el DAQ."

	try:
		daq = U3()
	except:
		print "ERROR: No se pude conectar con el daq."
		return


	while True:
		ekg = daq.getAIN(0)
		ekg_queue.put([ekg*70])

		sleep = .005

		daq.setFIOState(4, state=1)
		time.sleep(sleep)
		photo1 = daq.getAIN(1)
		daq.setFIOState(4, state=0)

		time.sleep(sleep)

		daq.setFIOState(6, state=1)
		time.sleep(sleep)
		photo2 = daq.getAIN(1)
		daq.setFIOState(6, state=0)

		R = (log10(fabs(photo1)) / log10(fabs(photo2)))

		#spo2 = 108.611 - 20.1389*R - 3.47222*R**2
		spo2 = R*100

		spo2_queue.put([spo2])

		#time.sleep(sleep)



if __name__ == "__main__":
	main()

