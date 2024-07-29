// AboutUs.js

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const AboutUs = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>About Us</Text>
      <Text style={styles.content}>
       Fit-Track is a mobile application designed to monitor fitness activities using the accelerometer sensor on users' devices.
       It allows real-time data collection, tracking movement patterns, intensity, and activity history. 
       With its intuitive interface and customizable settings, Fit-Track empowers users to monitor and improve their fitness journey conveniently.
      </Text>
      {/* Add more text or content here */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  content: {
    fontSize: 16,
    textAlign: 'center',
  },
});

export default AboutUs;
