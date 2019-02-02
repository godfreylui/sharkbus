import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('log.txt')

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
print min(log_time_step), max(log_time_step)


"""

do this all the time
    do this three times
        send message type 0
        wait 78 microsecond
        send message type 1
        wait 16000 microsecond
    then wait 32000 microsecond


"""
# send message type 0
# wait 78 microsecond
# send message type 1
# wait 78

# print log_time_step

# plt.plot(log_time_step)

# plt.plot(log_time-log_time_step)

# plt.show()