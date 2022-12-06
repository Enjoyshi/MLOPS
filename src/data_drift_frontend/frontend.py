import streamlit as st
import requests
import streamlit.components.v1 as components
import os

if __name__ == '__main__':
    st.title("Data Drift Monitor")

    st.write("This is a demo of the data drift monitor. The data is from the [Heart Disease UCI](https://www.kaggle.com/ronitf/heart-disease-uci) dataset. The model is a simple logistic regression model trained on the data. The data drift monitor is a simple implementation of the [Eurybia]")

    # Button to get the html report from the backend
    if st.button("Get data drift report"):
        api = os.environ['API_URL']
        r = requests.get(f"{api}/data_drift")
        
        # Display the html report
        components.html(r.text, height=1000)
        

