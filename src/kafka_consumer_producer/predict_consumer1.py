import joblib
import numpy as np
import pandas as pd
from utils import Consumer, Producer
import os

# data col : age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,slp,caa,thall

def load_model(path):
    return joblib.load(path)

def predict(data):
    model = load_model('svm_model.joblib')
    datas = pd.DataFrame(np.array([
        [data["age"]], [data["sex"]], [data["cp"]], [data["trtbps"]], [data["chol"]], [data["fbs"]], [data["restecg"]], [data["thalachh"]], [data["exng"]], [data["oldpeak"]], [data["slp"]], [data["caa"]], [data["thall"]]
        ]).T, columns=["age", "sex", "cp", "trtbps", "chol", "fbs", "restecg", "thalachh", "exng", "oldpeak", "slp", "caa", "thall"])
    datas.drop(columns=["chol","trtbps","fbs",'restecg'])
    pred = model.predict(datas)[0]
    return pred

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

if __name__ == "__main__":
    #server = '0.0.0.0:29092'
    server = os.environ['SERVERS_K']
    topic = 'ML'
    partition = 0

    consumer = Consumer(server, topic).consumer
    producer_save = Producer(server, 'Save').producer
    producer_alert = Producer(server, 'Alert').producer

    for msg in consumer:
        value = msg.value
        if not check_data(value):
            print("Data is not valid")
            continue
        pred = int(predict(value))
        pred_json = {"prediction": pred}
        save_data = {**value, **pred_json}
        print(save_data)
        producer_save.send('Save', save_data)
        if pred == 1:
            producer_alert.send('Alert', save_data)
            producer_alert.flush()
        producer_save.flush()