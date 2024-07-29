import React, { useEffect } from 'react';
import { View, Text, StyleSheet,Button } from 'react-native';
import DataCollection from '../services/DataCollectionService';
import { useNavigation } from '@react-navigation/native';
import {exportDataToCSV} from '../services/CSVService'


const CollectedData = () => {
  const accelerometerData = DataCollection();
  const navigation = useNavigation();

  useEffect(() => {
    // Set up interval to call exportCsv every 1 minute
    const interval = setInterval(() => {
      exportDataToCSV();
    }, 60000); // 60000 milliseconds = 1 minute


    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []); // Empty dependency array to run the effect only once on mount

  return (
    
    
    <View style={styles.container}>
      <Text style={styles.title}>Accelerometer Data:</Text>
      {accelerometerData && (
        <View style={styles.dataContainer}>
          <Text style={styles.dataText}>X: {accelerometerData.x}</Text>
          <Text style={styles.dataText}>Y: {accelerometerData.y}</Text>
          <Text style={styles.dataText}>Z: {accelerometerData.z}</Text>
          <Text style={styles.dataText}>Timestamp: {accelerometerData.timestamp}</Text>
        </View>
      )}
      <Button title=" Stop and Go Back" onPress={() => navigation.goBack()} /> 
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  dataContainer: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    borderRadius: 10,
  },
  dataText: {
    fontSize: 15,
    marginBottom: 7,
  },
});

export default CollectedData;
