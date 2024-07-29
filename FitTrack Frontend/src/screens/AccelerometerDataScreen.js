import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, Button } from 'react-native';
import * as SQLite from 'expo-sqlite';
import { exportDataToCSV } from '../services/CSVService'; // Import the CSV export function

const db = SQLite.openDatabase('accelerometer.db');

const AccelerometerDataScreen = () => {
  const [accelerometerData, setAccelerometerData] = useState([]);

  useEffect(() => {
    fetchAccelerometerData();
  }, []);

  const fetchAccelerometerData = () => {
    db.transaction((tx) => {
      tx.executeSql(
        'SELECT * FROM accelerometer_data;',
        [],
        (_, { rows }) => setAccelerometerData(rows._array),
        (_, error) => console.error('Error querying database', error)
      );
    });
  };

  const clearDatabase = () => {
    db.transaction((tx) => {
      tx.executeSql(
        'DELETE FROM accelerometer_data;',
        [],
        () => {
          console.log('Database cleared successfully');
          setAccelerometerData([]); // Clear the data state after clearing the database
        },
        (_, error) => console.error('Error clearing database', error)
      );
    });
  };

  const exportToCSV = () => {
    exportDataToCSV(); // Call the export function when exporting to CSV is triggered
  };

  return (
    <ScrollView>
      <View>
        <Button title="Export to CSV" onPress={exportToCSV} /> 
        <Button title="Clear Database" onPress={clearDatabase} />
        {accelerometerData.map((data, index) => (
          <View key={index}>
            <Text>X: {data.x}, Y: {data.y}, Z: {data.z}</Text>
            <Text>Timestamp: {data.timestamp}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
};

export default AccelerometerDataScreen;
