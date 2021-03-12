# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to load EGi file
"""

# %% some parms
import mne 
from mne import viz
import os 
'''
folder='C:\\Users\romar\Desktop\stas_ses_data\Subjects'
filename = 'RZ5_4code_20201126_174608.mff'
path =os.path.join(folder, filename)
#load the file 
raw = mne.io.read_raw_egi(folder + '\\' + filename)
'''
path = 'C:/Users/romar/Desktop/stas_ses_data/Subjects/RZ5_4code_20201126_174608.mff'
raw = mne.io.read_raw_egi(path)
# %% some analysis 
#select 1 channel 
raw = raw.copy().pick_channels(['E25', 'E38']) 
raw_loaded=raw.load_data()
raw_2 = mne.io.read_raw_egi(path)
#apply some filters
eeg_bp_freq = [0.3, 40]
raw_fil = raw.copy().filter(eeg_bp_freq[0], eeg_bp_freq[1])

# %% take a look
window_size = 30 #in sec
y_scale = {'eeg':10^-5, 'eog':10^-5} 
chan_2plot=['E25']
raw_fil.plot(duration=window_size, scalings=y_scale)

# %% Cutting the EGI file  to 5sec accroding to trig
events = mne.find_events(raw_2, stim_channel='STI 014') 
epochs = mne.Epochs(raw_fil, events, tmin=0, tmax=5,baseline=(0, 0))

epochs.plot()

# %% NOW WE WILL OPEN THE XTRODES FILE
# via matlab file
import scipy.io as sio

folder='C:\\Users\\romar\Desktop\stas_ses_data\ichilov_yuval_nir_pilot_afterCloud'
xtrodes_fname='data.mat'

path = os.path.join(folder,xtrodes_fname)

xtrodes_file=sio.loadmat(path)

xtrodes_data=xtrodes_file['data']
xtrodes_1 = xtrodes_data[(0,0)]










