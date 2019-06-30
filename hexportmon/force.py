import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('received.txt', sep='[', header=None)
log_time = []
msglist = []
idx = 0
time = df.iloc[:,0]
mess = df.iloc[:,1]

for i in range(len(df)):
    log_time.append(float(time[i].split(':')[-1]))
    msglist.append(mess[i].split(']')[0])

log_time = np.asarray(log_time)
log_time_step = np.diff(log_time)*1e6

for j in range(len(df)):
	a = msglist[j].split(', ')
	a = ['0x'+a[i][1:3]for i in range(len(a))]
	msglist[j] = a
print msglist
# '0x'+


 
