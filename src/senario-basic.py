from utils import Producer
import pandas as pd

server = 'localhost:9092'
topic = 'MachineLearning'

producer = Producer(server, topic).producer

data = pd.read_csv('data/test.csv')
data = data.drop(columns=['output'])

for i, row in data.iterrows():
    producer.send(topic, row.to_dict())
    producer.flush()