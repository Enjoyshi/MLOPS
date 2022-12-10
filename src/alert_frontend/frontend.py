# from utils import Consumer
import sys 
import streamlit as st
import os
import pandas as pd
import numpy as np

from utils import Consumer

def check_data(data):
    # check data type
    if not (type(data['age']) is int or type(data['age']) is float):
        return False
    if not (type(data['sex']) is int or type(data['sex']) is float):
        return False
    if not (type(data['cp']) is int or type(data['cp']) is float):
        return False
    if not (type(data['trtbps']) is int or type(data['trtbps']) is float):
        return False
    if not (type(data['chol']) is int or type(data['chol']) is float):
        return False
    if not (type(data['fbs']) is int or type(data['fbs']) is float):
        return False
    if not (type(data['restecg']) is int or type(data['restecg']) is float):
        return False
    if not (type(data['thalachh']) is int or type(data['thalachh']) is float):
        return False
    if not (type(data['exng']) is int or type(data['exng']) is float):
        return False
    if not (type(data['oldpeak']) is int or type(data['oldpeak']) is float):
        return False
    if not (type(data['slp']) is int or type(data['slp']) is float):
        return False
    if not (type(data['caa']) is int or type(data['caa']) is float):
        return False
    if not (type(data['thall']) is int or type(data['thall']) is float):
        return False
    return True

if __name__ == '__main__':
    
    server = os.environ['SERVERS_K']
    topic = 'Alert'
    consumer = Consumer(server, topic).consumer
    st.title("Alert Monitor")
    st.write("Patient data that is predicted to have heart disease")
    df =  pd.DataFrame(columns=['age', 'sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg', 'thalachh', 'exng', 'oldpeak', 'slp', 'caa', 'thall', 'prediction', 'timestamp'])
    my_table = st.empty()
    for msg in consumer:
        value = msg.value
        if not check_data(value):
            print("Invalid data")
            continue
        df = df.append(value, ignore_index=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by=['timestamp'], ascending=False)
        my_table.table(df)