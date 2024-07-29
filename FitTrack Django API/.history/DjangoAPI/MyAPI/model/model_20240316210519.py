
import pandas as pd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
#import the csv data from the react app.
data = pd.read_csv(r'C:\Users\Dell\Desktop\django\DjangoAPI\MyAPI\model\data.csv')
data.dropna(inplace=True)


# Convert to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')

print(data)

#calculate magnitude
data['Magnitude'] = np.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2)


# Calculate the frequency
time_diff = data['Timestamp'].diff().mode().dt.total_seconds()

print("Average frequency:", 1/time_diff)


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

input_data_with_g = data[['Magnitude']]
input_data_with_g['weight'] = 80
input_data_with_g['height'] = 165
input_data_with_g['age'] = 26
input_data_with_g['gender'] = 1.0

# g_u_data = input_data_with_g.copy()
# g_u_data.rename(columns={'Magnitude': 'userAcceleration'}, inplace=True)


# # Export the DataFrame as a CSV file
# g_u_data.to_csv('g_u_data.csv', index=False)

# g_u_data.head()

# u_data = input_data_without_g.copy()
# u_data.rename(columns={'a': 'userAcceleration'}, inplace=True)


# # Export the DataFrame as a CSV file
# u_data.to_csv('u_data.csv', index=False)

# u_data.head()
import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# %matplotlib inline

import zipfile
filename = 'archive.zip' #replace with your folder name
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall('./')

def read_data(path, filename):
    return pd.read_csv(os.path.join(path, filename), index_col=0)

df = read_data('./A_DeviceMotion_data/A_DeviceMotion_data/dws_1/', 'sub_1.csv')
df.head()

def produce_magnitude(df, column):
    df[column+'.mag'] = np.sqrt(df[column+'.x']**2 + df[column+'.y']**2 + df[column+'.z']**2)

produce_magnitude(df, 'userAcceleration')
produce_magnitude(df, 'rotationRate')
df.head()

import numpy as np
import pandas as pd

def get_ds_infos():
    """
    Read the file includes data subject information.

    Data Columns:
    0: code [1-24]
    1: weight [kg]
    2: height [cm]
    3: age [years]
    4: gender [0:Female, 1:Male]

    Returns:
        A pandas DataFrame that contains inforamtion about data subjects' attributes
    """

    dss = pd.read_csv("./data_subjects_info.csv")
    print("[INFO] -- Data subjects' information is imported.")

    return dss


def set_data_types(data_types=["userAcceleration"]):
    """
    Select the sensors and the mode to shape the final dataset.

    Args:
        data_types: A list of sensor data type from this list: [attitude, gravity, rotationRate, userAcceleration]

    Returns:
        It returns a list of columns to use for creating time-series from files.
    """
    dt_list = []
    for t in data_types:
        if t != "attitude":
            dt_list.append([t+".x",t+".y",t+".z"])
        else:
            dt_list.append([t+".roll", t+".pitch", t+".yaw"])
    print(dt_list)
    return dt_list


def creat_time_series(folder_name, dt_list, act_labels, trial_codes, mode="mag", labeled=True):
    """
    Args:
        folder_name: one of 'A_DeviceMotion_data', 'B_Accelerometer_data', or C_Gyroscope_data
        dt_list: A list of columns that shows the type of data we want.
        act_labels: list of activites
        trial_codes: list of trials
        mode: It can be 'raw' which means you want raw data
        for every dimention of each data type,
        [attitude(roll, pitch, yaw); gravity(x, y, z); rotationRate(x, y, z); userAcceleration(x,y,z)].
        or it can be 'mag' which means you only want the magnitude for each data type: (x^2+y^2+z^2)^(1/2)
        labeled: True, if we want a labeld dataset. False, if we only want sensor values.

    Returns:
        It returns a time-series of sensor data.

    """
    num_data_cols = len(dt_list) if mode == "mag" else len(dt_list*3)

    if labeled:
        dataset = np.zeros((0,num_data_cols+7)) # "7" --> [act, code, weight, height, age, gender, trial]
    else:
        dataset = np.zeros((0,num_data_cols))

    ds_list = get_ds_infos()

    print("[INFO] -- Creating Time-Series")
    for sub_id in ds_list["code"]:
        for act_id, act in enumerate(act_labels):
            for trial in trial_codes[act_id]:
                fname = folder_name+'/'+act+'_'+str(trial)+'/sub_'+str(int(sub_id))+'.csv'
                raw_data = pd.read_csv(fname)
                raw_data = raw_data.drop(['Unnamed: 0'], axis=1)
                vals = np.zeros((len(raw_data), num_data_cols))
                for x_id, axes in enumerate(dt_list):
                    if mode == "mag":
                        vals[:,x_id] = (raw_data[axes]**2).sum(axis=1)**0.5
                    else:
                        vals[:,x_id*3:(x_id+1)*3] = raw_data[axes].values
                    vals = vals[:,:num_data_cols]
                if labeled:
                    lbls = np.array([[act_id,
                            sub_id-1,
                            ds_list["weight"][sub_id-1],
                            ds_list["height"][sub_id-1],
                            ds_list["age"][sub_id-1],
                            ds_list["gender"][sub_id-1],
                            trial
                           ]]*len(raw_data), dtype=int)
                    vals = np.concatenate((vals, lbls), axis=1)
                dataset = np.append(dataset,vals, axis=0)
    cols = []
    for axes in dt_list:
        if mode == "raw":
            cols += axes
        else:
            cols += [str(axes[0][:-2])]

    if labeled:
        cols += ["act", "id", "weight", "height", "age", "gender", "trial"]

    dataset = pd.DataFrame(data=dataset, columns=cols)
    return dataset
#________________________________


ACT_LABELS = ["dws","ups", "wlk", "jog", "std", "sit"]
TRIAL_CODES = {
    ACT_LABELS[0]:[1,2,11],
    ACT_LABELS[1]:[3,4,12],
    ACT_LABELS[2]:[7,8,15],
    ACT_LABELS[3]:[9,16],
    ACT_LABELS[4]:[6,14],
    ACT_LABELS[5]:[5,13]
}

sdt = [ "userAcceleration"]
print("Selected sensor data types:\n" + str(sdt))
dt_list = set_data_types(sdt)
print("\nSelected columns from dataset:\n" + str(dt_list))

ACT_LABELS = ["sit", "std", "dws", "ups", "wlk", "jog"]
act_labels = ACT_LABELS [0:6]  # all activities
print("Selected activites: " + str(act_labels))

TRIAL_CODES = {
    ACT_LABELS[0]:[5,13],
    ACT_LABELS[1]:[6,14],
    ACT_LABELS[2]:[1,2,11],
    ACT_LABELS[3]:[3,4,12],
    ACT_LABELS[4]:[7,8,15],
    ACT_LABELS[5]:[9,16],
}

TRIAL_CODES = {
    ACT_LABELS[0]:[5],
    ACT_LABELS[1]:[6],
    ACT_LABELS[2]:[1],
    ACT_LABELS[3]:[3],
    ACT_LABELS[4]:[7],
    ACT_LABELS[5]:[9],
}
trial_codes = [TRIAL_CODES[act] for act in act_labels]
print("[INFO] -- Selected trials: " + str(trial_codes))

print("Loading...")
dataset = creat_time_series("./A_DeviceMotion_data/A_DeviceMotion_data", dt_list, act_labels, trial_codes, mode="mag", labeled=True)
print("Finished!")
dataset.head()

dataset.to_csv('dataset.csv', index=False)
#stop from here and run rest on collab because jupiter might get slow for this data

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

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report

from sklearn.metrics import classification_report
#for this previous code
# Step 1: Prepare the Data
X = dataset.drop(columns=['act', 'id', 'trial'])  # Features
y = dataset['act']  # Target labels

# Step 2: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Step 4: Evaluate the Model
y_pred = rf_model.predict(X_test)

# Calculate classification report
report = classification_report(y_test, y_pred, target_names=ACT_LABELS)
print(report)

X.head()

np.unique(y_pred)

#testing the preprocessed data.

df_u = pd.read_csv('u_data (2).csv')
df_g_u = pd.read_csv('g_u_data (2).csv')

# Step 4: Evaluate the Model
df_u_pred = rf_model.predict(df_u)

df_g_u_pred = rf_model.predict(df_g_u)

len(df_u)

out_u = np.unique(df_u_pred)
for i in out_u:
  print(ACT_LABELS[int(i)])

out_g_u = np.unique(df_g_u_pred)
for i in out_g_u:
  print(ACT_LABELS[int(i)])

def mode(arr):
    unique, counts = np.unique(arr, return_counts=True)
    max_count_idx = np.argmax(counts)
    return unique[max_count_idx]

print("Mode of the prediction without gravity: ",ACT_LABELS[int(mode(out_u))])
print("Mode of the prediction with gravity: ",ACT_LABELS[int(mode(out_g_u))])