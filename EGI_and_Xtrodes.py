# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to load EGi file
"""
import mne
from mne import viz
import os
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import copy
import yaml
import pandas as pd
from visbrain.gui import Sleep

# importing configuration file
with open("egi_conf.yml") as conf_yaml:
    conf = yaml.safe_load(conf_yaml)


# %% some parms
path = conf["Path_egi"]
#load the fil
raw_orig = mne.io.read_raw_egi(path)

# %% some analysis
#select 1 channel
raw = copy.deepcopy(raw_orig).pick_channels(['E25'])

raw_loaded=raw.load_data()
# a=['E25','E38','E61','E190','E244','E248','E249','E257']
#apply some filters
eeg_bp_freq = [0.3, 40]
raw_fil = raw_loaded.copy().filter(eeg_bp_freq[0], eeg_bp_freq[1])

# %% take a look
window_size = 30 #in sec
y_scale = {'eeg':10^-5, 'eog':10^-5}
raw_fil.plot(duration=window_size,scalings=y_scale)
events = mne.find_events(raw_orig,stim_channel='STI 014') 
epochs = mne.Epochs(raw_fil, events, tmin=0, tmax=5,baseline=(0, 0))

epochs.plot()
ls = list()
for i in range(1, len(epochs.events)):
    ls.append(epochs.events[i][0] - epochs.events[i-1][0])


'''
# %% NOW WE WILL OPEN THE XTRODES FILE
# via matlab file
import scipy.io as sio

folder='C:\\Users\\romar\Desktop\stas_ses_data\ichilov_yuval_nir_pilot_afterCloud'
xtrodes_fname='data.mat'

path = os.path.join(folder,xtrodes_fname)

xtrodes_data=sio.loadmat(path)
xtrodes_file=sio.loadmat(path)

xtrodes_data=xtrodes_file['data']
xtrodes_1 = xtrodes_data[(0,0)]

folder='C:\\Users\\romar\Desktop\stas_ses_data\ichilov_yuval_nir_pilot_afterCloud'
xtrodes_fname='events.mat'

path = os.path.join(folder,xtrodes_fname)

xtrodes_data=sio.loadmat(path)
xtrodes_file=sio.loadmat(path)

xtrodes_data=xtrodes_file['events']
xtrodes_1 = xtrodes_data[(0,0)]
'''
# %%NOW WE WILL OPEN THE XTRODES FILE
# via matlab file


folder = conf["Path_xt"]
xtrodes_fname = 'data.mat'
xtrodes_events_fname = 'events.mat'

path = os.path.join(folder, xtrodes_fname)
path_ev = os.path.join(folder, xtrodes_events_fname)

xtrodes_file = sio.loadmat(path)
xtrodes_ev = sio.loadmat(path_ev)

data_out=np.empty([8, 495616])
for i in range(0, 7):
    data_out[i, :] = xtrodes_file['data']['Ch'+str(i)][0][0] # xample to load one channel

CH0 = data_out[0, :]
CH1 = data_out[1, :]
CH2 = data_out[2, :]
CH3 = data_out[3, :] #This is the signal we will use for comparison
CH4 = data_out[4, :]
CH5 = data_out[5, :]
CH6 = data_out[6, :]
CH7 = data_out[7, :]

events_xtrodes = xtrodes_ev['events']['event_time'][0][0]
# data=xtrodes_data['data']
np.diff(events)

#%%plottting

CH3 = sp.signal.resample(CH3, int(len(CH3)/4))
t_x = np.linspace(0, len(CH3)/1000, len(CH3))
raw_fil_data = raw_fil._data
t_EGI = np.linspace(0, len(raw_fil_data)/1000, len(raw_fil_data))
plt.plot(t_x, CH3, t_EGI, raw_fil_data )
#plt.plot(data_out[4,1:20000]) # let's plot 5sec

# %%Displaying the Xtrodes signal in visbrain

'''
# load EDF in to Sleep
hfile=None # if there is no
folder= 'C://Users//romar/Desktop/stas_ses_data'
EDF_file='data_record_0.edf'
path=os.path.join(folder,EDF_file)
#cfg_file = ''
Sleep(path).show()
# %%Playing with Pandas
'''

s = pd.Series(epochs.events, index = [np.linspace(0, 18, 19)])





