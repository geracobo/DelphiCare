#!/usr/bin/env python
# encoding utf-8


import time
from daq import DAQ
from server import Server
import random


daq = DAQ()
server = Server('localhost', 8090)


analog1 = 0
analog2 = 0


def main():
	volts = 200
	delta = 0
	while(True):
		server.send_voltage(volts)
		delta = random.randint(-1, 1)
		volts = volts + delta
		time.sleep(.01)

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

