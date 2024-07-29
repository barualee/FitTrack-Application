import { queryDataFromDatabase, clearDatabase } from './DatabaseService';
import * as FileSystem from 'expo-file-system';
import axios from 'axios';

const exportDataToCSV = async () => {
    try {
        const data = await queryDataFromDatabase();
      
        const csvData = formatDataToCSV(data);
        const json_data = {'file': csvData}
        try {
                const apiUrl = 'http://172.20.10.8:5000/api/prediction'; // Replace with your Flask API endpoint
                await axios.post(apiUrl, json_data)
                   .then(response => {
                   console.log('Response:',response);
               })
               .catch(error => {
                   console.error('Error:', error.message);
       });
            }
       catch (error) {
           console.error('Error:', error.message);
       }
      
        console.log('Formatted CSV data:', csvData);
        //  print(csvData)
        // Check if csvData is valid
        if (!csvData || csvData.trim() === '') {
            console.error('CSV data is empty.');
            return;
        }

        // // Specify the directory path where the file will be saved
        // const directoryPath = FileSystem.documentDirectory + 'Download/';
        // // Create the directory if it doesn't exist
        // await FileSystem.makeDirectoryAsync(directoryPath, { intermediates: true });

        // // Specify the file path
        // const filePath = directoryPath + 'accelerometer_data.csv';

        // let combinedData = csvData; // Initialize combined data with new data
        // // Check if file exists
        // const fileInfo = await FileSystem.getInfoAsync(filePath);
        // if (fileInfo.exists) {
        //     // Read existing data
        //     const existingData = await FileSystem.readAsStringAsync(filePath);
        //     // Combine existing data with new data
        //     combinedData = existingData + '\n' + csvData;
        // }

        // // Write combined data to the file (appending to existing data)
        // await FileSystem.writeAsStringAsync(filePath, combinedData, { encoding: FileSystem.EncodingType.UTF8, append: true });

        // console.log('CSV file written successfully:', filePath);
        
        
        
        // Clear the database after successful export
        clearDatabase();

    } catch (error) {
        console.error('Error exporting data:', error);
    }
};

// Function to format data into CSV format
const formatDataToCSV = (data) => {
    if (!data || data.length === 0) {
        return ''; // Return empty string if no data
    }

    // Header row
    let csv = 'X,Y,Z,Timestamp\n';

    // Iterate over each data entry and append to CSV
    data.forEach((entry) => {
        csv += `${entry.x},${entry.y},${entry.z},${entry.timestamp}\n`;
    });

    return csv;
};

export { exportDataToCSV };
