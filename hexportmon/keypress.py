import pandas as pd
# import uspp
from SerialPort_linux import SerialPort
import copy
import time
import numpy as np
import cPickle as pickle
from datetime import datetime
import keyboard
from sharkmon import SharkMonitor

for1 = pd.read_csv('../data/for1.csv')
right = pd.read_csv('../data/right.csv')
left = pd.read_csv('../data/left.csv')
back = pd.read_csv('../data/back.csv')
rest = pd.read_csv('../data/rest.csv')
# print(for1.iloc[:,0])

def main(input):

    shm = SharkMonitor(ser=SerialPort("/dev/ttyUSB0", 1000, 38400))

    time0 = datetime.now() 


    for i in range(len(input)):

        while True:
            time1 = datetime.now() 
            sent_dt = time1 - time0
            if sent_dt.microseconds >= input.iloc[i,0]:
                time0 = time1
                break

        shm_msg_to_be_send = shm.SendMessage(message_type=input.iloc[i,1], message=input.iloc[i,2])


import sys, termios, tty, os, time
 
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == '__main__':

	# main(rest)
	while True:

		char = getch()
		main(rest)

		if (char == 'p'):
			print('stop')
			exit(0)

		if (char == 'w'):
			print('forward')


