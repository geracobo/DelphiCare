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
	temp_queue = multiprocessing.Queue()
	spo2_queue = multiprocessing.Queue()
	alarm_queue = multiprocessing.Queue()

	print "Creando procesos de comunicación..."
	st = multiprocessing.Process(target=server_process, args=(ekg_queue, temp_queue, spo2_queue, alarm_queue))
	dt = multiprocessing.Process(target=daq_process, args=(ekg_queue, temp_queue, spo2_queue, alarm_queue))

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
		if cmd == "alarm on":
			alarm_queue.put(True)
		if cmd == "alarm off":
			alarm_queue.put(False)
		parse_cmd(cmd)


	print "Terminando procesos..."
	st.terminate()
	dt.terminate()

def parse_cmd(cmd):
	if(cmd == ""):
		pass


def server_process(ekg_queue, temp_queue, spo2_queue, alarm_queue):
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
		if not temp_queue.empty():
			packet['temp'] = temp_queue.get()
		if not spo2_queue.empty():
			packet['spo2'] = spo2_queue.get()
			print packet['spo2']


		if not alarm_queue.empty():
			alarm_state = alarm_queue.get()
			print alarm_state
			if alarm_state == True:
				print "Prendiendo Alarma..."
				packet['alarm'] = 'on'
			else:
				print "Apagando Alarma..."
				packet['alarm'] = 'off'

		packetJson = json.dumps(packet)

		#print "Mandando Paquete: ", packetJson
		server.send(str(packetJson)+"|")
		time.sleep(.01)

def daq_process(ekg_queue, temp_queue, spo2_queue, alarm_queue):
	"""
	This thread communicates with the daq.
	"""
	from u3 import U3
	from math import log, fabs, log10

	print "Conectandose con el DAQ."

	try:
		daq = U3()
	except:
		print "ERROR: No se pude conectar con el daq."
		return

	alarm_state = False

	while True:

		# Read Alarm
		al = daq.getFIOState(7)

		# Check if there was a change in state
		#if al != alarm_state:
		#	alarm_queue.put(al)
		#	alarm_state = al


		if al:
			alarm_queue.put(True)

		# Read EKG
		ekg = daq.getAIN(0)
		ekg_queue.put([ekg*70])


		# Read Temp
		temp = daq.getAIN(2)
		temp_queue.put([temp])

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

		R = log(fabs(photo1)) / log(fabs(photo2))

		#spo2 = 108.611 - 20.1389*R - 3.47222*R**2
		spo2 = R*100

		spo2_queue.put([spo2])

		time.sleep(sleep)



if __name__ == "__main__":
	main()

