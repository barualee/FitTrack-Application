import React from "react";
import { Text, StyleSheet, View } from "react-native";
import { Button } from "react-native-paper";
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';
const HomeScreen = () => {
  const navigation = useNavigation();

  const goToReadCSVScreen = () => {
    navigation.navigate('ReadCSV');
  };

  const goToCollectedData = () => {
    navigation.navigate('CollectData');
  };

  const goToAccelerometerDatabase = () => {
    navigation.navigate('AccelerometerData');
  };

  const goToAboutUs = () => {
    navigation.navigate('AboutUs');
  };
  const goToGraphs = () => {
    navigation.navigate('Graphs');
  };


  return (
    <View style={styles.container}>
      <Text style={styles.text}>Fit-Track app</Text>
      <Button mode="contained" style={styles.button} onPress={goToReadCSVScreen}>
        Recorded Values
      </Button>
      <Button mode="contained" style={styles.button} onPress={goToCollectedData}>
        Collect Acc. Data
      </Button>
      <Button mode="contained" style={styles.button} onPress={goToAccelerometerDatabase}>
        Check Database
      </Button>
      <Button mode="contained" style={styles.button} onPress={goToAboutUs}>
        About Us
      </Button>
      <Button mode="contained" style={styles.button} onPress={goToGraphs}>
        Movement Graph
      </Button>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff", // Set background color to white
  },
  text: {
    fontSize: 40,
    marginBottom: 20, // Add some spacing below the text
  },
  button: {
    marginVertical: 10, // Add vertical margin between buttons
    width: 200, // Set a fixed width for the buttons
  },
});

export default HomeScreen;
