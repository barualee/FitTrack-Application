import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/HomeScreen';
import AccelerometerDataScreen from '../screens/AccelerometerDataScreen';
import ReadCSVScreen from '../screens/CSVScreen';
import CollectedData from '../screens/DataCollectorScreen';

const Tab = createBottomTabNavigator();

const BottomTabNavigator = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Accelerometer" component={AccelerometerDataScreen} />
      <Tab.Screen name="ReadCSV" component={ReadCSVScreen} />
      <Tab.Screen name="CollectData" component={CollectedData} />
    </Tab.Navigator>
  );
};

export default BottomTabNavigator;
