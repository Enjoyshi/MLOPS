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
    api = "http://localhost:80"

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

if st.button("Get AUC Report"):
    #api = os.environ['API_URL']
    api = "http://localhost:80"

    data = json.dumps({"Download": True})
    r = requests.post(f"{api}/data_drift", data= data)

    # Display the html report
    components.html(r.text, height=800)
    


