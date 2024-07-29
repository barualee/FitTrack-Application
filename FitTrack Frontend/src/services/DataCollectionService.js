import { useState, useEffect } from 'react';
import { initDatabase, insertData } from './DatabaseService';
import { startAccelerometer, stopAccelerometer } from './AccelerometerService'; // Import the accelerometer functions

const DataCollection = () => {
  const [accelerometerData, setAccelerometerData] = useState(null);

  useEffect(() => {
    // Initialize the database when the component mounts
    initDatabase();

    // Start collecting accelerometer data
    const subscription = startAccelerometer((data) => {
      // Callback function to receive accelerometer data
      // Update the accelerometer data state
      setAccelerometerData(data);

      // Insert the accelerometer data into the database
      insertData(data);
    });

    // Return a cleanup function to stop the accelerometer subscription when the component unmounts
    return () => {
      stopAccelerometer(subscription);
    };
  }, []);

  return accelerometerData; // Return the accelerometer data obtained from the subscription
};

export default DataCollection;