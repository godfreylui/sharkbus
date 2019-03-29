import  uspp
import numpy as np
import pandas as pd
import cPickle as pickle
# import matplotlib.pyplot as plt
from sharkmon import SharkMonitor

# ser= uspp.SerialPort("/dev/ttyUSB0", 1000, 38400)

shm = SharkMonitor(ser=None)

def get_times():

    df = pd.read_csv('../data/log1.txt')

    log_time = []

    idx = 0

    while True:
        try:
            log_time.append(float(df.iloc[idx,0].split(':')[-1].split('[')[0]))
            idx += 1
        except Exception as e:
            print "I am done"
            break

    log_time = np.asarray(log_time)

    log_time_step = np.diff(log_time)*1e6

    return log_time_step


def get_messages():

    data = open('../data/log1.txt','r')

    shm_msgs = []

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

        shm_msg = shm.SendMessage(message_type=10, message=combined_message)

        print "Original message \n", msg

        print "Hex string message \n", hex_string_message
        
        print "Char string message \n", char_string_message

        print "Combined message \n", combined_message

        print "Sharkmon message \n", shm_msg

        print  "********************"

        shm_msgs.append(shm_msg)

    return shm_msgs

    
def main():

    log_time_step =  get_times()

    shm_msgs = get_messages()
    


if __name__ == '__main__':
    main()