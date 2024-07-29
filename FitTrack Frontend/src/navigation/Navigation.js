import React from 'react';
import { Text, StyleSheet, View } from "react-native";
import { createDrawerNavigator } from '@react-navigation/drawer';
import HomeScreen from '../screens/HomeScreen';
import AccelerometerDataScreen from '../screens/AccelerometerDataScreen';
import ReadCSVScreen from '../screens/CSVScreen';
import CollectedData from '../screens/DataCollectorScreen';
import AboutUs from '../screens/AboutUs';
import MovementMinutesGraph from '../screens/Graphs'

const Drawer = createDrawerNavigator();

const Navigation = () => {
  return (
    <Drawer.Navigator >
      <Drawer.Screen name="Home" component={HomeScreen} />
      <Drawer.Screen name="AccelerometerData" component={AccelerometerDataScreen} />
      <Drawer.Screen name="ReadCSV" component={ReadCSVScreen} />
      <Drawer.Screen name="CollectData" component={CollectedData} />
      <Drawer.Screen name="AboutUs" component={AboutUs} />
      <Drawer.Screen name="Graphs" component={MovementMinutesGraph} />
    </Drawer.Navigator>
  );
};


export default Navigation;