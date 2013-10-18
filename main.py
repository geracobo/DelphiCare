#!/usr/bin/env python
# coding=utf-8


import time
import thread
import threading
import random


analog1 = 0
analog2 = 0


global should_exit
should_exit = False
server_done = threading.Event()
daq_done = threading.Event()

def main():
	global should_exit
	print "Creando procesos de comunicación..."
	try:
		st = threading.Thread(target=server_thread)
		dt = threading.Thread(target=daq_thread)

		st.start()
		time.sleep(.5)
		dt.start()
	except:
		print "ERROR: No se pudieron crear los procesos de comunicación."

	cmd = ""
	while(cmd != "salir"):
		cmd = raw_input()
		parse_cmd(cmd)

	should_exit = True

	print "Esperando a que cierre el proceso del servidor..."
	server_done.wait()
	print "Esperando a que cierre el proceso del daq..."
	daq_done.wait()

	print "Good Bye!"


def parse_cmd(cmd):
	if(cmd == ""):
		pass


def server_thread():
	"""
	This thread communicates with the server.
	"""
	global should_exit

	from server import Server
	print "Conectandose con el servidor..."
	server = Server('localhost', 8090)

	if not server.connected:
		return


	volts = 200
	delta = 0
	while not should_exit:
		#server.send_voltage(volts)
		#delta = random.randint(-1, 1)
		#volts = volts + delta
		time.sleep(0)

	print "Proceso de comunicación con el servidor terminado."

def daq_thread():
	"""
	This thread communicates with the daq.
	"""
	global should_exit

	from daq import DAQ
	print "Conectandose con el DAQ."
	daq = DAQ()

	if not daq.connected:
		return



	while not should_exit:
		pass

	print "Proceso de comunicación con el DAQ terminado."

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

