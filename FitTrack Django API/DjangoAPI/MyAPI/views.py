from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv,os,json,pickle
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import numpy as np

def getGroupedReadings(df, current_timestamp):
    # Group by 'action' and calculate the sum of 'timeDiff'
    grouped = df.groupby('Output')['Time diff'].sum().reset_index()

    # Convert the grouped DataFrame to dictionary
    time_diff_sum_dict = dict(zip(grouped['Output'], grouped['Time diff']))

    # Create the result dictionary
    result = {
        'TimeStamp': current_timestamp,
        'durations': time_diff_sum_dict
    }
    
    return result

def preprocessing(data):
            print(data)
            data.dropna(inplace=True)

            data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
            data['Magnitude'] = np.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2)
            return data

def set_cors_headers(response):
  response['Access-Control-Allow-Origin'] = '*'
  response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Add allowed methods
  response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # Add allowed headers
  return response
# Create your views here.

def parse_csv_from_json(csv_data):
    # Parse CSV data from the JSON payload
    csv_list = csv_data.splitlines()
    csv_reader = csv.reader(csv_list)
    csv_data = []
    for row in csv_reader:
        csv_data.append(row)
    return csv_data

client = MongoClient('mongodb+srv://avineykhetarpal01:Cricket01@cluster0.ekr78qi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['COEN691']
collection = db['fit-track']

@csrf_exempt
def getData(request):
    try:
        #get only today date's readings
        # Get today's date
        today_date_string = datetime.now().strftime('%Y-%m-%d')

        # Define the start and end of today as strings
        start_of_day_string = today_date_string + "_00:00:00"
        end_of_day_string = today_date_string + "_23:59:59"

        # Query documents with TimeStamp within today's date range
        query = {
            'TimeStamp': {
                '$gte': start_of_day_string,
                '$lt': end_of_day_string
            }
        }
        documents=collection.find(query)
        document_list = [doc for doc in documents]

    # Convert list of dictionaries to JSON
        json_data = json.dumps(document_list, default=str)
        #print(json_data)
        return JsonResponse({'message':json_data})
    except Exception as e:
        print({f"error! {e}"})
        return JsonResponse({'message':f"An error occurred: {e}"})  


@csrf_exempt
def prediction(request):
     
    if request.method =="POST":
        data_str = request.body.decode('utf-8')
        json_data = json.loads(data_str)
        filedata = json_data.get('file', '')
        try:
            directory = "/Users/n.k.barua/Desktop/Fittrack-server/DjangoAPI/MyAPI/model/raw_data"
            current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            if not os.path.exists(directory):
              os.makedirs(directory)
            filename = f"data_{current_timestamp}.csv"
            
            with open(os.path.join(directory ,filename), 'w') as f:
             f.write(filedata)
            data=pd.read_csv(os.path.join(directory,filename))
            data.dropna(inplace=True)
            data.drop_duplicates(subset=['Timestamp'], inplace=True)
            data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
            data['Magnitude'] = np.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2)
            data['weight'] = 80
            data['height'] = 165
            data['age'] = 26
            data['gender'] = 1.0
            time_diff=data['Timestamp'].diff()
            time_diff = time_diff.dropna()
            time_difff =  time_diff.mode()[0].total_seconds()
            sampling_rate = 1 / time_difff
            data=data.drop(columns=['X','Y','Z','Timestamp'])
            data.rename(columns={'Magnitude': 'userAcceleration'}, inplace=True)
            
            directory2 = "/Users/n.k.barua/Desktop/Fittrack-server/DjangoAPI"
            filename2 = "model.pkl"
            with open(os.path.join(directory2 ,filename2), 'rb') as file:
                loaded_model = pickle.load(file)
            y_pred2= loaded_model.predict(data)
            ACT_LABELS = ["sit", "std", "dws", "ups", "wlk", "jog"]
            predicted_activities = [ACT_LABELS[int(prediction)] for prediction in y_pred2]

            # Combine the Series and list into a DataFrame
            df = pd.concat([time_diff.dt.total_seconds(), pd.Series(predicted_activities)], axis=1)
            df.columns = ['Time diff', 'Output']
            df = df.dropna()
            
            #convert to groupby activity with time interval.
            data_dict = getGroupedReadings(df, current_timestamp)
            #data_dict = df.to_dict(orient='records')
            #store in mongoDB
            collection.insert_one(data_dict)
            #print(data_dict)
            
            return JsonResponse({'message':'Successfully received CSV'})
        except Exception as e:
         return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

    #   if 'file' not in request.json:
    #    print(request.body)
    #   csv_data = request.json['file']
    #   try:
    #    parsed_data = parse_csv_from_json(csv_data)
        
    #     # Export CSV data to a file named "raw.csv" in a directory
    #     directory = "/Users/Dell/Desktop/django/"
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
        
    #     # Get current timestamp
    #     current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    #     # Generate filename with current timestamp
    #     filename = f"data_{current_timestamp}.csv"
    #     with open(os.path.join(directory, filename), "w", newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerows(parsed_data)
        
        return JsonResponse({'message': 'Successfully received CSV'})
    #   except Exception as e:
        # return JsonResponse({'error': str(e)}), 400
    # else:
        #  return JsonResponse({'error'}), 400