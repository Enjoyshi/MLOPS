# from utils import Consumer
import sys 
import streamlit as st
import os
import pandas as pd
import numpy as np
# import Consumer from utils.py
#sys.path.append(os.path.abspath(os.path.join('..')))

from utils import Consumer

if __name__ == '__main__':
    server = os.environ['SERVERS_K']
    #server = 'localhost:9092'
    topic = 'Alert'
    consumer = Consumer(server, topic).consumer
    st.title("Alert Monitor")
    st.write("Patient data that is predicted to have heart disease")
    df =  pd.DataFrame(columns=['age', 'sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg', 'thalachh', 'exng', 'oldpeak', 'slp', 'caa', 'thall', 'prediction'])
    my_table = st.empty()
    for msg in consumer:
        value = msg.value
        print(value)
        df = df.append(value, ignore_index=True)
        my_table.table(df)