from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv,os,json,pickle
from datetime import datetime
import pandas as pd
import numpy as np

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

@csrf_exempt
def prediction(request):
     
    if request.method =="POST":
        data_str = request.body.decode('utf-8')
        json_data = json.loads(data_str)
        filedata = json_data.get('file', '')
        try:
            directory = "/Users/Dell/Desktop/django/DjangoAPI/MyAPI/datasheet"
            current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            if not os.path.exists(directory):
              os.makedirs(directory)
            filename = f"data_{current_timestamp}.csv"
            with open(os.path.join(directory ,filename), 'w') as f:
             f.write(filedata)
            data=pd.read_csv(os.path.join(directory ,filename))
            # print(data)
            data.dropna(inplace=True)
            
            data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
            data['Magnitude'] = np.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2)
            data['weight'] = 80
            data['height'] = 165
            data['age'] = 26
            data['gender'] = 1.0
            time_diff = data['Timestamp'].diff().mode().dt.total_seconds()
            data=data.drop(columns=['X','Y','Z','Timestamp'])
            data.rename(columns={'Magnitude': 'userAcceleration'}, inplace=True)
            directory2 = "/Users/Dell/Desktop/django/DjangoAPI/MyAPI"
            filename2 = "model.pkl"
            with open(os.path.join(directory2 ,filename2), 'rb') as file:
                loaded_model = pickle.load(file)
            y_pred2= loaded_model.predict(data)
            ACT_LABELS = ["dws","ups", "wlk", "jog", "std", "sit"]
            predicted_activities = [ACT_LABELS[int(prediction)] for prediction in y_pred2]
            print(y_pred2)
            print(predicted_activities)
            
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