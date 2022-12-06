from utils import Producer
import pandas as pd
import numpy as np

server = 'localhost:9092'
topic = 'ML'

producer = Producer(server, topic).producer

data = pd.read_csv('data/test.csv')
data = data.drop(columns=['output'])

# add random data to each column
data['age'] = data['age'] + np.random.randint(100, 200, data.shape[0])
# data['sex'] = data['sex'] + np.random.randint(0, 2, data.shape[0])
data['cp'] = data['cp'] + np.random.randint(0, 4, data.shape[0])
data['trtbps'] = data['trtbps'] + np.random.randint(100, 200, data.shape[0])
data['chol'] = data['chol'] + np.random.randint(100, 200, data.shape[0])
data['fbs'] = data['fbs'] + np.random.randint(0, 2, data.shape[0])
data['restecg'] = data['restecg'] + np.random.randint(0, 2, data.shape[0])
data['thalachh'] = data['thalachh'] + np.random.randint(100, 200, data.shape[0])
data['exng'] = data['exng'] + np.random.randint(0, 2, data.shape[0])
data['oldpeak'] = data['oldpeak'] + np.random.randint(0, 2, data.shape[0])
data['slp'] = data['slp'] + np.random.randint(0, 3, data.shape[0])
data['caa'] = data['caa'] + np.random.randint(0, 4, data.shape[0])
data['thall'] = data['thall'] + np.random.randint(0, 3, data.shape[0])


for i, row in data.iterrows():
    producer.send(topic, row.to_dict())
    producer.flush()