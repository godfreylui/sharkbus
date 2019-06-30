import uspp
import copy
import time
import numpy as np
import cPickle as pickle
from datetime import datetime
# import matplotlib.pyplot as plt
from sharkmon import SharkMonitor


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

    # plt.plot(log_time_step, 'r')
    # plt.plot(log_time_step_bkup, 'g')
    # plt.show()

    return log_time_step


def get_messages():

    data = open('../data/for1.txt','r')

    shm_msgs = []
    msg_types = []
    ori_msgs = []
    hex_msgs = []

    while True:

        line = data.readline()

        if len(line) == 0:
            break

        msg =  line.split('[', 1)[1].split(']')[0].split(',')

        hex_string_message = [ hex(int("0x"+m.split("'")[1], 16)) for m in msg]

        char_string_message = [ chr(int("0x"+m.split("'")[1], 16)) for m in msg]

        combined_message = char_string_message[0] 

        for k in range(1, len(char_string_message)):
            combined_message += char_string_message[k]

        msg_type = ord(char_string_message[0])%16

        # shm_msg = shm.SendMessage(message_type=msg_type, message=combined_message)

        # print "Original message \n", msg

        # print "Hex string message \n", hex_string_message
        
        # print "Char string message \n", char_string_message

        # print "Combined message \n", combined_message

        # print "Sharkmon message \n", shm_msg

        # print "Message Type \n", msg_type

        # print  "********************"

        # raw_input()

        shm_msgs.append(combined_message)
        msg_types.append(msg_type)
        ori_msgs.append(msg)
        hex_msgs.append(hex_string_message)

    return msg_types, shm_msgs, ori_msgs, hex_msgs


# def left():

#     data = open('../data/left.txt')

def main():

    shm = SharkMonitor(ser=uspp.SerialPort("/dev/ttyUSB0", 1000, 38400))

    log_time_steps =  get_times()
    msg_types, shm_msgs, ori_msgs, hex_msgs = get_messages()

    time0 = datetime.now() 


    for i, (dt, msg_type, shm_msg, ori_msg) in enumerate(zip(log_time_steps, msg_types, shm_msgs, ori_msgs)):

        while True:
            time1 = datetime.now() 
            sent_dt = time1 - time0
            if sent_dt.microseconds >= dt:
                time0 = time1
                break

        shm_msg_to_be_send = shm.SendMessage(message_type=msg_type, message=shm_msg)
        # print hex_msgs[i]
        # print "sent_dt at:", datetime.now(), shm_msg_to_be_send
        # shm_decode_msg = shm.DecodeMessage(shm_msg_to_be_send)

        # print "ori \n", ori_msg
        # print "shm \n", shm_decode_msg
        # raw_input()

        # print "Sent message \t", i, "original dt", dt, "send dt", sent_dt


if __name__ == '__main__':

    main()