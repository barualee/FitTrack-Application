import axios from 'axios'

// Define a function to fetch data
async function fetchData() {
    try {
        // Make the HTTP request to get the data
        const response = await axios.get('http://172.20.10.8:5000/api/getdata');
        // Return the response data as an object
        return response.data.message;
    } catch (error) {
        // If an error occurs, log it and return null
        console.error('Error fetching data:', error);
        return null;
    }
}
async function sumValues() {

    const data = await fetchData();
    
    // Convert JSON string to JavaScript object (list of dictionaries)
    const listOfDicts = JSON.parse(data);

    const groupedValues = groupActionDuration(listOfDicts);
    // Return the resulting dictionary with summed values
    return groupedValues;
  }

function groupActionDuration(listOfDicts){
    const myDictionary = {
        low: 0.0,
        medium: 0.0,
        high: 0.0,
        latestTimeStamp: new Date(0) 
      };
    // Iterate over each dictionary in the list and log its contents
    listOfDicts.forEach((dict, index) => {
        const dateString = dict.TimeStamp;

    // Split the string into date and time components
    const [datePart, timePart] = dateString.split('_');
    const [year, month, day] = datePart.split('-');
    const [hours, minutes, seconds] = timePart.split('-');

    // Construct a Date object using the components
    const date = new Date(year, month - 1, day, hours, minutes, seconds);

        const dict_date = new Date(date);

        if (dict_date > myDictionary.latestTimeStamp) {
            myDictionary.latestTimeStamp = dict_date;
        }
        // Iterate over the durations in the dictionary
        for (const [key, value] of Object.entries(dict.durations)) {
            // Check if the key is "sit"
            if (key === "sit" || key === "std") {
                // Add the value to the "low" key in myDictionary
                myDictionary.low += Number(value.toFixed(2));
            } else if (key === "wlk" || key === "ups" || key === "dws") {
                // Add the value to the "medium" key in myDictionary
                myDictionary.medium += Number(value.toFixed(2));
            } else {
                myDictionary.high += Number(value.toFixed(2));
            }
        }
    });
    return myDictionary;
  }
export default sumValues;
  