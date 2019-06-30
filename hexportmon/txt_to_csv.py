import pandas as pd
import numpy as np
import csv
import uspp
import copy
import time
import cPickle as pickle
from datetime import datetime
# import matplotlib.pyplot as plt
# from sharkmon import SharkMonitor

with open('received.txt', 'r+') as old:
	with open('newreceived.txt','w') as new:
		while True:

			line = old.readline()
			if len(line)==0:
				break
			
			line = line.replace(", '0F'", "")
			new.write(line)

file = 'rest'

def get_times():

    data = open('../data/'+file+'.txt','r')

    log_time = []

    idx = 0

    while True:

        line = data.readline()

        if len(line) == 0:
            break

        log_time.append(float(line.split(':')[-1].split('[')[0]))

    log_time = np.asarray(log_time)

    #the first delta t is zero
    log_time_step = np.hstack([0.0, np.diff(log_time)*1e6])

    log_time_step_bkup = copy.deepcopy(log_time_step)

    for i, delta_t in enumerate(log_time_step):
        if 15000 < delta_t < 16200:
            log_time_step[i] = 16000
        if 50 < delta_t < 100:
            log_time_step[i] = 50
    
    return log_time_step

def get_messages():

    data = open('../data/'+file+'.txt','r')

    shm_msgs = []
    msg_types = []
    ori_msgs = []
    hex_msgs = []

    while True:

        line = data.readline()

        if len(line) == 0:
            break

        msg =  line.split('[', 1)[1].split(']')[0].split(',')

        # hex_string_message = [ hex(int("0x"+m.split("'")[1], 16)) for m in msg]

        char_string_message = [ chr(int("0x"+m.split("'")[1], 16)) for m in msg]

        combined_message = char_string_message[0] 

        for k in range(1, len(char_string_message)):
            combined_message += char_string_message[k]

        msg_type = ord(char_string_message[0])%16

        shm_msgs.append(combined_message)
        msg_types.append(msg_type)
        # ori_msgs.append(msg)
        # hex_msgs.append(hex_string_message)

    return msg_types, shm_msgs #, ori_msgs, hex_msgs


def main():

	log_time_steps =  get_times()
	msg_types, shm_msgs = get_messages()


	with open('../data/'+file+'.csv', 'w') as old:

		thewriter = csv.writer(old)
		thewriter.writerow(['log_time_step', 'msg_types', 'shm_msgs'])
    	
    	# for i, (dt, msg_type, shm_msg) in enumerate(zip(log_time_steps, msg_types, shm_msgs)):
		for i in range(len(log_time_steps)):

			thewriter.writerow([log_time_steps[i], msg_types[i], shm_msgs[i]])


if __name__ == '__main__':

	main()