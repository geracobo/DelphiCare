#!/usr/bin/env python
# encoding utf-8


import time
import u3
import socketIO_client

try:
	daq = u3.U3()
except:
	print "Error al conectarse al DAQ."


socket = socketIO_client.SocketIO('delphicare.nodejitsu.com', 80)

analog1 = 0
analog2 = 0


def main():
	while(True):
		#onda()
		socket.emit('voltaje', {'valor': 10})
		time.sleep(1)

def onda():
	daq.setFIOState(4, state=1)
	time.sleep(0.1)
	analog1 = daq.getAIN(0)
	daq.setFIOState(4, state=0)

	time.sleep(0.1)

	daq.setFIOState(5, state=1)
	time.sleep(0.1)
	analog2 = daq.getAIN(1)
	daq.setFIOState(5, state=0)

	time.sleep(0.1)



if __name__ == "__main__":
	main()

