# -*- coding: utf-8 -*-
"""fit_track_data_preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BWv69kkVo99flm_UKnOdPyo0gFLCcw2E
"""

import pandas as pd
import numpy as np

#import the csv data from the react app.
data = pd.read_csv('accelerometer_data-NEW.csv')
data.dropna(inplace=True)

data

# Convert to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')

print(data)

#calculate magnitude
data['Magnitude'] = np.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2)
data

# Calculate the frequency
time_diff = data['Timestamp'].diff().mode().dt.total_seconds()

print("Average frequency:", 1/time_diff)

#frequency analysis
from scipy import fftpack
import matplotlib.pyplot as plt

for column in ['X','Y','Z','Magnitude']:
  sample = data[column]
  y = sample.values
  N = y.size # data size
  T = 1.0 / 10 # inverse of sampling rate
  x = np.linspace(0.0, N*T, N)
  yf = np.abs(fftpack.fft(y))
  xf = fftpack.fftfreq(N, d=T)

  fig, ax = plt.subplots()
  ax.plot(np.abs(xf), np.abs(yf))
  #truncate x axis.
  ax.set_xlim(0, 10)
  plt.show()
  print()

#magnitude plot

plt.figure(figsize=(12, 6))
plt.plot(data['Timestamp'], data['Magnitude'], label='Magnitude of the signal')
plt.xlabel('Timestamp')
plt.ylabel('Magntiude Signal Amplitude')
plt.legend()
plt.show()

#filter gravity
from scipy.signal import butter, freqz, filtfilt

def lowpass_filter(data, low_cut_off=0.5, fs=10):
    b, a = butter(4, low_cut_off, fs=fs, btype='lowpass', analog=False)
    y = filtfilt(b, a, data)
    return b, a, y

#obtain gravity component
b,a,data['x_g'] = lowpass_filter(data['X'].values, low_cut_off=0.5, fs=10)

b,a,data['y_g'] = lowpass_filter(data['Y'].values, low_cut_off=0.5, fs=10)

b,a,data['z_g'] = lowpass_filter(data['Z'].values, low_cut_off=0.5, fs=10)

data['x_u'] = data['X'] - data['x_g']
data['y_u'] = data['Y'] - data['y_g']
data['z_u'] = data['Z'] - data['z_g']

#limit the plot to 10 seconds
data.head(4000).plot(x='Timestamp', y=['X', 'x_g', 'x_u'], figsize=(20,10))
data.head(4000).plot(x='Timestamp', y=['Y', 'y_g', 'y_u'], figsize=(20,10))
data.head(4000).plot(x='Timestamp', y=['Z', 'z_g', 'z_u'], figsize=(20,10))

#user accelration
data['a'] = np.sqrt(data['x_u']*data['x_u']+data['y_u']*data['y_u']+data['z_u']*data['z_u'])

data.head()

#input_data_without_g = data[['Timestamp', 'a']]
input_data_without_g = data[['a']]
input_data_without_g['weight'] = 80
input_data_without_g['height'] = 165
input_data_without_g['age'] = 26
input_data_without_g['gender'] = 1.0


#input_data_with_g = data[['Timestamp', 'Magnitude']]
input_data_with_g = data[['Magnitude']]
input_data_with_g['weight'] = 80
input_data_with_g['height'] = 165
input_data_with_g['age'] = 26
input_data_with_g['gender'] = 1.0

g_u_data = input_data_with_g.copy()
g_u_data.rename(columns={'Magnitude': 'userAcceleration'}, inplace=True)


# Export the DataFrame as a CSV file
g_u_data.to_csv('g_u_data.csv', index=False)

g_u_data.head()

u_data = input_data_without_g.copy()
u_data.rename(columns={'a': 'userAcceleration'}, inplace=True)


# Export the DataFrame as a CSV file
u_data.to_csv('u_data.csv', index=False)

u_data.head()