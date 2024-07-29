#filter gravity
from scipy.signal import butter, freqz, filtfilt
import pandas as pd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import os

data = pd.read_csv(r'C:\Users\Dell\Desktop\django\DjangoAPI\MyAPI\model\data.csv')
data.dropna(inplace=True)

data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
data['Magnitude'] = np.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2)

time_diff = data['Timestamp'].diff().mode().dt.total_seconds()

# for column in ['X','Y','Z','Magnitude']:
#   sample = data[column]
#   y = sample.values
#   N = y.size # data size
#   T = 1.0 / 10 # inverse of sampling rate
#   x = np.linspace(0.0, N*T, N)
#   yf = np.abs(fftpack.fft(y))
#   xf = fftpack.fftfreq(N, d=T)
#   fig, ax = plt.subplots()
#   ax.plot(np.abs(xf), np.abs(yf))
#   ax.set_xlim(0, 10)
#   plt.show()
#   print()

plt.figure(figsize=(12, 6))
plt.plot(data['Timestamp'], data['Magnitude'], label='Magnitude of the signal')
plt.xlabel('Timestamp')
plt.ylabel('Magntiude Signal Amplitude')
plt.legend()
# plt.show()

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
# data.head(4000).plot(x='Timestamp', y=['X', 'x_g', 'x_u'], figsize=(20,10))
# data.head(4000).plot(x='Timestamp', y=['Y', 'y_g', 'y_u'], figsize=(20,10))
# data.head(4000).plot(x='Timestamp', y=['Z', 'z_g', 'z_u'], figsize=(20,10))

#user accelration
data['a'] = np.sqrt(data['x_u']*data['x_u']+data['y_u']*data['y_u']+data['z_u']*data['z_u'])
# data.head()

input_data_without_g = data[['a']]
input_data_without_g['weight'] = 80
input_data_without_g['height'] = 165
input_data_without_g['age'] = 26
input_data_without_g['gender'] = 1.0
input_data_with_g = data[['Magnitude']]
input_data_with_g['weight'] = 80
input_data_with_g['height'] = 165
input_data_with_g['age'] = 26
input_data_with_g['gender'] = 1.0

