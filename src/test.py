from utils import Consumer, Producer

server = 'localhost:9092'
topic = 'Save'
consumer = Consumer(server, topic).consumer

for msg in consumer:
    print(msg.value)