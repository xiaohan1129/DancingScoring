#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np
def read_vital(filename):
    with open(filename, 'r') as f:
        data = f.read()
    
    data_split = data.split('\n')[:-1]
    
    n = len(data_split)
    signals = []
    bpms = []
    
    for i in range(n):
        line = data_split[i]
        
        if line[1:7] == 'Signal':
            signal = int(line[10:])
            signals.append(signal)
            continue
        elif line[1:4] == 'BPM':
            bpm = int(line[5:])
            bpms.append(bpm)
            continue
    
    bpm_mean = np.mean(np.array(bpms))
    return signals, bpms, bpm_mean
#
#
#
#
# # In[17]:
#
#
# signals, bpms, bpm = read_vital("512.log")
#
#
# # In[18]:
#
#
# bpm
#
#
# # In[19]:
#
#
# bpms

