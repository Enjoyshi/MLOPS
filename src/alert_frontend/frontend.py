# from utils import Consumer
import sys 
import streamlit as st
import os
import pandas as pd
import numpy as np
# import Consumer from utils.py
#sys.path.append(os.path.abspath(os.path.join('..')))

from utils import Consumer

def check_data(data):
    # check data type
    if type(data['age']) != int or type(data['age']) != float:
        return False
    if type(data['sex']) != int or type("sex") != float:
        return False
    if type(data['cp']) != int or type(data['cp']) != float:
        return False
    if type(data['trtbps']) != int or type(data['trtbps']) != float:
        return False
    if type(data['chol']) != int or type(data['chol']) != float:
        return False
    if type(data['fbs']) != int or type(data['fbs']) != float:
        return False
    if type(data['restecg']) != int or type(data['restecg']) != float:
        return False
    if type(data['thalachh']) != int or type(data['thalachh']) != float:
        return False
    if type(data['exng']) != int or type(data['exng']) != float:
        return False
    if type(data['oldpeak']) != int or type(data['oldpeak']) != float:
        return False
    if type(data['slp']) != int or type(data['slp']) != float:
        return False
    if type(data['caa']) != int or type(data['caa']) != float:
        return False
    if type(data['thall']) != int or type(data['thall']) != float:
        return False
    return True

if __name__ == '__main__':
    server = os.environ['SERVERS_K']
    #server = 'localhost:9092'
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
        my_table.table(df)