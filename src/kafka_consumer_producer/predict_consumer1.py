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
        pred = int(predict(value))
        pred_json = {"prediction": pred}
        save_data = {**value, **pred_json}
        print(save_data)
        producer_save.send('Save', save_data)
        if pred == 1:
            producer_alert.send('Alert', save_data)
            producer_alert.flush()
        producer_save.flush()