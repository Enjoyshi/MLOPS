import streamlit as st
import requests
import streamlit.components.v1 as components
import os
import csv
import json
import datetime
import pandas as pd
import numpy as np


def add_row_to_csv(path, row, fieldnames=["auc", "timestamp"]):
    # Create a new csv file if it doesn't exist
    if not os.path.exists(path):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
            writer.writerow(row)
    else:
        with open(path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)



st.title("Data Drift Monitor")

st.write("This is a demo of the data drift monitor. The data is from the [Heart Disease UCI](https://www.kaggle.com/ronitf/heart-disease-uci) dataset. The model is a SVM model trained on the data. The data drift monitor is a simple implementation of the [Eurybia]")

# Create a line chart to display the AUC
df = pd.read_csv("auc.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index('timestamp')
st.line_chart(df)

my_metric = st.empty()
value = None
delta = None
my_metric.metric(label="AUC" , value=value, delta=delta)
# Button to get the AUC
if st.button("Get AUC"):
    #api = os.environ['API_URL']
    api = "http://localhost:8000"

    # Json data to send to the API
    data = json.dumps({"Download": False})

    # Send the request
    r = requests.post(f"{api}/data_drift", data=data)
    if r.status_code != 200:
        st.write("Error getting AUC")
        st.write(r.text)
    else:
        # Get the response
        response = json.loads(r.text)

        # Add the AUC to the csv file
        add_row_to_csv("auc.csv", [response['auc'], datetime.datetime.now()])
        # Calculate the delta
        with open("auc.csv", 'r') as f:
            reader = csv.reader(f)
            next(reader,None)
            data = list(reader)
            data = [float(x[0]) for x in data]
            if (len(data) == 1):
                d = 0
            else:
                d = data[-1] - data[-2]
            
        value = response['auc']
        delta = d
        my_metric.metric(label="AUC", value=value, delta=delta)

start = st.date_input("Start Date", datetime.datetime.now())
end = st.date_input("End Date", datetime.datetime.now())

if st.button("Get CSV Data"):
    #api = os.environ['API_URL']
    api = "http://localhost:8000"

    data = json.dumps({"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")})
    r = requests.post(f"{api}/get_data", data= data)
    if r.status_code != 200:
        st.write("Error getting AUC")
        st.write(r.text)
    else:
        # Get the response
        response = json.loads(r.text)
        result = response['result']
        df =  pd.DataFrame(columns=['age', 'sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg', 'thalachh', 'exng', 'oldpeak', 'slp', 'caa', 'thall', 'prediction', 'timestamp'])
        for i in result:
            df = df.append(i, ignore_index=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Download the csv file
        csv = df.to_csv(index=True).encode('utf-8')

        # Download the csv file
        st.write("CSV file is ready to download, click the button below to download the file.")
        my_download = st.download_button("Download Data", data=csv, file_name="data.csv", mime="text/csv")
    

if st.button("Get AUC Report"):
    #api = os.environ['API_URL']
    api = "http://localhost:8000"

    data = json.dumps({"Download": True})
    r = requests.post(f"{api}/data_drift", data= data)

    # Display the html report
    components.html(r.text, height=800)
    


