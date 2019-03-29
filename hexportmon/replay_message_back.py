import  uspp
import copy
import numpy as np
import cPickle as pickle
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from sharkmon import SharkMonitor

# ser= uspp.SerialPort("/dev/ttyUSB0", 1000, 38400)

shm = SharkMonitor(ser=None)

def get_times():

    data = open('../data/log1.txt','r')

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
        if 15000 < delta_t < 16000:
            log_time_step[i] = 15900
        if 50 < delta_t < 100:
            log_time_step[i] = 70

    plt.plot(log_time_step, 'r')
    plt.plot(log_time_step_bkup, 'g')
    plt.show()
    raw_input()

    return log_time_step


def get_messages():

    data = open('../data/log1.txt','r')

    shm_msgs = []
    msg_types = []

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
    return msg_types, shm_msgs


def main():

    log_time_steps =  get_times()
    print log_time_steps
    msg_types, shm_msgs = get_messages()

    # print "length of log_time_steps \t", len(log_time_steps)
    # print "length of shm_msgs \t", len(shm_msgs)
    
    # print msg_types
    # print shm_msgs

if __name__ == '__main__':
    main()