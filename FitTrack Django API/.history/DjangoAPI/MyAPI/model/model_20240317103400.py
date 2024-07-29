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
data['a'] = np.sqrt(data['x_u']*data['x_u']+data['y_u']*data['y_u']+data['z_u']*data['z_u'])

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

# model
dataset=pd.read_csv("")
plt.rcParams['figure.figsize'] = (30,8)
plt.rcParams['font.size'] = 32
plt.rcParams['image.cmap'] = 'plasma'
plt.rcParams['axes.linewidth'] = 2
clr1 = ["rs-","r*-","ro-","rv-","rp-","r^-"]
clr2 = ["bs-","b*-","bo-","bv-","bp-","b^-"]
act_lbl = ["Sat", "Stand-Up", "Downstairs", "Upstairs", "Walking", "Jogging"]
lbl = ["rotation", "acceleration"]

period = 2.5 # Seconds
sample_rate = 50 # Hz
points = int(period*sample_rate)
x_ticks = np.arange(0.,points/sample_rate,1./sample_rate)
print("Data points per time-series: " + str(points))

act_data = np.zeros((6,points))
fig, ax = plt.subplots(1, 6, sharex='col', sharey='row')
uid = 12 # We have 24 users in the dataset, uid can be selected from {0,1,...23}
for i in np.unique(dataset["act"]):
    i =int(i)
    data = dataset[(dataset["id"] == uid) & (dataset["act"] == i)]
    acc = data["userAcceleration"].values

    acc = acc[:points]


    if i!=0:

        ax[i].plot(x_ticks, acc, "b^-", linewidth=2, markersize=8)
    else:

        ax[i].plot(x_ticks, acc, "b^-", linewidth=2, markersize=12, label=lbl[1])

    ax[i].set_title(act_lbl[i])
plt.setp(ax, yticks=np.arange(0, 11, 2))
fig.text(0.5, 0.004, 'second', ha='center')
fig.text(0.075, 0.5, 'magnitude value', va='center', rotation='vertical', )
ax[0].legend(loc="upper center", fontsize = 20)