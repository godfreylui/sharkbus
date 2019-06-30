import  uspp
import copy
import time
import numpy as np
import cPickle as pickle
from datetime import datetime
from sharkmon import SharkMonitor
import keyboard

# data = open('../data/for1.txt','r')
# class readtxt:
def get_times():

    data = open('../data/for1.txt','r')
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
    
    data = open('../data/for1.txt','r')
    shm_msgs = []
    msg_types = []

    while True:

        line = data.readline()

        if len(line) == 0:
            break

        msg =  line.split('[', 1)[1].split(']')[0].split(',')

        char_string_message = [ chr(int("0x"+m.split("'")[1], 16)) for m in msg]

        combined_message = char_string_message[0] 

        for k in range(1, len(char_string_message)):
            combined_message += char_string_message[k]

        msg_type = ord(char_string_message[0])%16

        shm_msgs.append(combined_message)
        msg_types.append(msg_type)

    return msg_types, shm_msgs
def get_times1():

    data = open('../data/left.txt','r')
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


def get_messages1():

    data = open('../data/left.txt','r')
    shm_msgs = []
    msg_types = []

    while True:

        line = data.readline()

        if len(line) == 0:
            break

        msg =  line.split('[', 1)[1].split(']')[0].split(',')

        char_string_message = [ chr(int("0x"+m.split("'")[1], 16)) for m in msg]

        combined_message = char_string_message[0] 

        for k in range(1, len(char_string_message)):
            combined_message += char_string_message[k]

        msg_type = ord(char_string_message[0])%16

        shm_msgs.append(combined_message)
        msg_types.append(msg_type)

    return msg_types, shm_msgs

def main():

    shm = SharkMonitor(ser=uspp.SerialPort("/dev/ttyUSB0", 1000, 38400))

    log_time_steps =  get_times()
    msg_types, shm_msgs = get_messages()
    left_log_time_steps =  get_times1()
    left_msg_types, left_shm_msgs = get_messages1()


    time0 = datetime.now() 

    for i, (dt, msg_type, shm_msg) in enumerate(zip(log_time_steps, msg_types, shm_msgs)):

        while True:
            time1 = datetime.now() 
            sent_dt = time1 - time0
            if sent_dt.microseconds >= dt:
                time0 = time1
                break

        shm_msg_to_be_send = shm.SendMessage(message_type=msg_type, message=shm_msg)

        while True:
            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                    for i, (dt, msg_type, shm_msg) in enumerate(zip(left_log_time_steps, left_msg_types, left_shm_msgs)):

                        while True:
                            time1 = datetime.now() 
                            sent_dt = time1 - time0
                            if sent_dt.microseconds >= dt:
                                time0 = time1
                                break

                        shm_msg_to_be_send = shm.SendMessage(message_type=msg_type, message=shm_msg)

                    break  # finishing the loop
                else:
                    pass
            except:
                break  
            
if __name__ == '__main__':

    main()
# data = open('../data/for1.txt','r')
# readtxt(data).main
