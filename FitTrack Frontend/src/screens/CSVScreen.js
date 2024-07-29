import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, Button , StyleSheet} from 'react-native';
import * as FileSystem from 'expo-file-system';
import Papa from 'papaparse';


const ReadCSVScreen = () => {
  const [csvData, setCSVData] = useState([]);

  useEffect(() => {
    readCSV();
  }, []);

  const readCSV = async () => {
    try {
      const path = FileSystem.documentDirectory + 'Download/accelerometer_data.csv';
      const fileInfo = await FileSystem.getInfoAsync(path);
      if (fileInfo.exists) {
        const content = await FileSystem.readAsStringAsync(path);
        const result = Papa.parse(content, { header: true });
        setCSVData(result.data);
      } else {
        console.log('CSV file does not exist.');
      }
    } catch (error) {
      console.error('Error reading CSV file:', error);
    }
  };

  const clearCSV = async () => {
    try {
      const path = FileSystem.documentDirectory + 'Download/accelerometer_data.csv';
      await FileSystem.deleteAsync(path);
      setCSVData([]); // Clear the CSV data state after clearing the file
    } catch (error) {
      console.error('Error clearing CSV file:', error);
    }
  };

  return (
    <ScrollView>
    <View>
    <Button title="Clear CSV Data" onPress={clearCSV} style={styles.button} />
      {csvData.map((row, index) => (
        <View key={index}>
          <Text>X: {row.X}, Y: {row.Y}, Z: {row.Z}, Timestamp: {row.Timestamp}</Text>
        </View>
      ))}
    </View>
    </ScrollView>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  button: {
    marginBottom: 10,
  },
  rowContainer: {
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    paddingVertical: 10,
  },
  rowText: {
    fontSize: 16,
  },
});

export default ReadCSVScreen;
