#!/usr/bin/env python
# encoding utf-8


import time
import u3
import httplib

daq = u3.U3()

con = httplib.HTTPConnection('delphicare.herokuapp.com')
con.connect()

analog1 = 0
analog2 = 0


def main():
	#while(True):
		#onda()
	con.request('POST', '/voltaje', 'voltaje=10', {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"})
	con.getresponse()


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

