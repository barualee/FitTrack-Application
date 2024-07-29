// BlankBarChart.js
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { BarChart} from "react-native-gifted-charts";
import sumValues  from '../services/GraphCalculator'

const MovementMinutesGraph = () => {

    const [data, setData] = useState(null); // State to store the fetched data
    useEffect(() => {
        // Define an asynchronous function inside useEffect to fetch and sum the data
        const fetchDataAndSum = async () => {
            try {
                const summedData = await sumValues(); // Call sumValues to get the summed data
                setData(summedData); // Set the fetched and summed data in state
            } catch (error) {
                console.error('Error fetching and summing data:', error);
            }
        };

        // Call the function to fetch and sum the data
        fetchDataAndSum();
    }, []);
    
    // Conditional rendering to show a loading indicator while waiting for data
    if (data === null) {
        return (
            <View style={styles.container}>
                <Text style={styles.heading}>Loading Graph...</Text>
            </View>
        );
    }
    
    const formattedTimeStamp = data.latestTimeStamp.toLocaleString() !== (new Date(0).toLocaleString())
    ? data.latestTimeStamp.toLocaleString('en-US')
    : new Date().toLocaleString('en-US');

    const movement_minutes = (data.medium/60) + (data.high/60)

    const targetString = movement_minutes <= 100
    ? 'Dont give up! \nYou still have '+(Math.round(100 - movement_minutes))+' minutes to achieve 100 healthy movement minutes.'
    : 'Congratulations! \nYou have crossed the day target of 100 movement minutes.';

    const barData = [
        {value: (data.low/60), label: 'Sedentary', frontColor: '#05ED98'},
        {value: (data.medium/60), label: 'Walking', frontColor: '#0F52BA'},
        {value: (data.high/60), label: 'Running', frontColor: '#FF0000'},
    ];
    return (
    <View style={styles.container}>
        <Text style={styles.chartContainer}>{targetString}</Text> 
        <View style={styles.container}>   
        <Text style={styles.heading}>Movement Minutes For Today</Text>
        <View style={styles.chartContainer}>
            <BarChart
                barWidth={22}
                noOfSections={3}
                barBorderRadius={4}
                frontColor="lightgray"
                data={barData}
                yAxisThickness={0}
                xAxisThickness={0}
                spacing={50}
                backgroundColor={'#71797E'}
            />
        </View>
        <Text style={styles.footnote}>Last Updated: {formattedTimeStamp}</Text>
        </View>
        </View>
    )};


    const styles = StyleSheet.create({
        container: {
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
        },
        heading: {
          fontSize: 24,
          fontWeight: 'bold',
          textAlign: 'center',
        },
        footnote: {
            fontSize: 15,
            fontWeight: 'regular',
            marginBottom: 20,
            marginTop: 50,
            textAlign: 'center',
          },
        chartContainer: {
          width: '80%', // Adjust the width as needed
          height: 10, // Adjust the height as needed
        },
        chartContainer: {
            width: 300, // Adjust the width as needed
            flexWrap: 'wrap',
            textAlign: 'center',
            fontSize: 15,
            fontWeight: 'bold',
            marginTop: 40,
          },
      });
export default MovementMinutesGraph;
