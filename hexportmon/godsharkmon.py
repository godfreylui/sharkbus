#!/usr/bin/python

# SharkBus protocol decoder/analyser
# Based on the SharkBus RS485 Communication Protocol from Dynamic Controls
# For protocol information contact dynamiccontrols.com
# Special thanks to Warren Pettigrew for his assistance. 
# Author: James Conner
# Date: 27th September 2010


import os, sys, string, time, datetime, gmpy, uspp, pygame, ctypes

class SharkMonitor:
	def __init__(self):
		self.ser = uspp.SerialPort("/dev/ttyUSB0", 1000, 38400)
		self._msg = None


	# Read bytes until we get the End-of-Transmission byte (0x0F)
	def ReceiveMessage(self):
		msg = []
		messagebytes = ""
		lasthexvalue = "00"
		while lasthexvalue != "0F":
			if self.ser.inWaiting():
				data = self.ser.read(1)
			#if data:
				hexvalue = "%02X"%ord(data)
				# if lasthexvalue == "0F" : # 0x0F is the End of Transmission byte.
				# 	print
				# 	print datetime.datetime.now(),
				# print hexvalue,
				msg.append(hexvalue)
				messagebytes = messagebytes + data
				lasthexvalue = hexvalue
 
		self._msg = msg
		return(messagebytes)

	# Send a message, terminated with parity byte and the End-of-Transmission byte (0x0F)
	def SendMessage(self, message_type, message):
		message_length = len(message)-1 # The start byte contains the message length (00 = 1byte) and message_type
		start_byte = chr((message_length << 4)+message_type)
		message = start_byte + message
		# print message_type
		# print message
		parity = 0
		for data in message:
			parity=parity+(ord(data)&127)
		parity = (255-(parity & 127))
		parity_byte = chr(parity)
		message = message + parity_byte # Add the parity on to the end
		message = message + chr(15) # Add the EoT byte to the end.
		print "Sending Message at", datetime.datetime.now()
		self.ser.write(message)
		
		return()

	def TimedMessage(self, message_type1, message1, message_type2, message2):
		start_time = datetime.datetime.now()
		sent_78_mu = False
		count = 0		
		while True:
			send_78_mu = datetime.datetime.now()-start_time
			if not sent_78_mu  and (70< send_78_mu.microseconds):
				SharkMonitor().SendMessage(message_type1, message1)
				start_time = datetime.datetime.now()
				sent_78_mu = True
			
			send_16_ms = datetime.datetime.now()-start_time
			if sent_78_mu  and  (15950 < send_16_ms.microseconds):
				SharkMonitor().SendMessage(message_type2, message2)
				start_time = datetime.datetime.now()
				sent_78_mu = False
				count += 1
				if 5 > count >= 3:
					sent_78_mu = True

				elif count == 5:
					sent_78_mu = False
					count = 0


	# Decode messages into human readable form.
	def DecodeMessage(self,message):
		print "Received at:", datetime.datetime.now(), self._msg
		for data in message:
			hexvalue = "%02X"%ord(data)
		if ord(message[0]) == 0:
			# print "Framing/Power-on startup message - Chomp"
			message = message[1:]
		# The start of message bytes all have bit 7 clear - Every other message byte has bit 7 set.
		if  ord(message[0]) > 127 or ord(message[0]) == 15:
			# print "Not at message start"
			return(0)
		messagetype=(ord(message[0]) & 0x0F)

		# print self._msg
		# raw_input()

		if messagetype == 0 : # Shark Remote General Information (Joytstick Data)
			joy_speed = ((ord(message[1]) & 127)<<3)+((ord(message[4]) & 56)>>3)
			joy_dir = ((ord(message[2]) & 127)<<3)+(ord(message[4]) & 7)
			speed_pot = ((ord(message[3]) & 127)<<1)+((ord(message[4]) & 64)>>6)
			# print "\n\n\n\n\n"
			# print "Type:",0, "Y:", joy_speed, "X:", joy_dir, "Speed:", speed_pot
			# print "Message \t", self._msg
			# print "\n\n\n\n\n"


		if messagetype == 1 : # Shark Power Module General Information
			fuel_guage = ord(message[1]) & 31
			horn = ord(message[3]) & 1
			driving_mode = ord(message[6]) & 15
			speedo = ord(message[7]) & 31
			# print "\n\n\n\n\n"
			# print "Type:", 1, "Batt:", fuel_guage, "Horn:", horn, "Mode:", driving_mode, "Speedo:", speedo
			# print "Message \t", self._msg
			# print "\n\n\n\n\n"

		if messagetype == 2 : # SR HHP Data
			print "SR HHP Data"

		if messagetype == 3 : # SPM HHP Data
			print "SPM HHP Data"

		if messagetype == 4 : # SR Power Up Information
			print "SR Power Up Information"
			remote_type = ord(message[1]) & 127
			year_of_manufacture = 2000+(ord(message[2]) & 127)
			month_of_manufacture = ord(message[3]) & 15
			serial_number = ((ord(message[4]) & 127) << 14) + ((ord(message[5]) & 127) << 7) + (ord(message[6]) & 127)
			software_major = (ord(message[7]) & 56) >> 3
			software_minor = ord(message[7]) & 7
			capabilities = ord(message[8]) & 127
			print "Remote Type:", remote_type
			print "Manufactured:", month_of_manufacture, "/", year_of_manufacture
			print "Serial:", serial_number
			print "Software:"+str(software_major)+"."+str(software_minor)
			print "Capabilites:", capabilities

		if messagetype == 5 : # SPM Power Up Information
			print "SPM Power Up Information"
			capabilities = ord(message[1]) & 127
			print "Capabilities:",capabilities

		if messagetype == 6 : # Joystick Calibration
			print "Joystick Calibration (SR or ACU)"

		if messagetype == 7 : # Factory Test
			print "Factory Test"

		if messagetype == 8 : # SACU General Information
			print "SACU General Information"

		if messagetype == 9 : # SACU Power Up Information
			print "SACU Power Up Information"

		if messagetype == 10 : # SPM Programmable Settings
			print "SPM Programmable Settings"

		return(messagetype)

MyMonitor = SharkMonitor()
start_time = datetime.datetime.now()
sent_78_mu = False
count = 0
while True:

	messagebytes = MyMonitor.ReceiveMessage()
	MyMonitor.DecodeMessage(messagebytes)
