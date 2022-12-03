from kafka import KafkaProducer
import json


# data col : age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,slp,caa,thall
# data : 57,1,0,150,276,0,0,112,1,0.6,1,1,1

producer = KafkaProducer(bootstrap_servers='localhost:29092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))

partitioner = 0

for i in range(10):
    partitioner = 1 if partitioner == 0 else 0
    msg = {"age": 57, "sex": 1, "cp": 0, "trtbps": 150, "chol": 276, "fbs": 0, "restecg": 0, "thalachh": 112, "exng": 1, "oldpeak": 0.6, "slp": 1, "caa": 1, "thall": 1}
    producer.send('ML', msg)
    producer.flush()