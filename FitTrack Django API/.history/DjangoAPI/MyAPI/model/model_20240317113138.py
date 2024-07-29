#filter gravity
from scipy.signal import butter, freqz, filtfilt
import pandas as pd
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
# data = pd.read_csv(r'C:\Users\Dell\Desktop\django\DjangoAPI\MyAPI\model\data.csv')
# data.dropna(inplace=True)

# data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
# data['Magnitude'] = np.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2)

# time_diff = data['Timestamp'].diff().mode().dt.total_seconds()
# def lowpass_filter(data, low_cut_off=0.5, fs=10):
#     b, a = butter(4, low_cut_off, fs=fs, btype='lowpass', analog=False)
#     y = filtfilt(b, a, data)
#     return b, a, y

# #obtain gravity component
# b,a,data['x_g'] = lowpass_filter(data['X'].values, low_cut_off=0.5, fs=10)
# b,a,data['y_g'] = lowpass_filter(data['Y'].values, low_cut_off=0.5, fs=10)
# b,a,data['z_g'] = lowpass_filter(data['Z'].values, low_cut_off=0.5, fs=10)

# data['x_u'] = data['X'] - data['x_g']
# data['y_u'] = data['Y'] - data['y_g']
# data['z_u'] = data['Z'] - data['z_g']
# data['a'] = np.sqrt(data['x_u']*data['x_u']+data['y_u']*data['y_u']+data['z_u']*data['z_u'])

# input_data_without_g = data[['a']]
# input_data_without_g['weight'] = 80
# input_data_without_g['height'] = 165
# input_data_without_g['age'] = 26
# input_data_without_g['gender'] = 1.0
# input_data_with_g = data[['Magnitude']]
# input_data_with_g['weight'] = 80
# input_data_with_g['height'] = 165
# input_data_with_g['age'] = 26
# input_data_with_g['gender'] = 1.0

# model
dataset=pd.read_csv(r"C:\Users\Dell\Desktop\django\DjangoAPI\MyAPI\model\dataset.csv")

X = dataset.drop(columns=['act', 'id', 'trial'])  # Features
y = dataset['act']  # Target labels

# Step 2: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Step 4: Evaluate the Model
y_pred = rf_model.predict(X_test)


