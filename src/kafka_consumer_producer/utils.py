from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import TopicPartition
import json

class Consumer:
    def __init__(self, server, topic, if_partition = False, partition = 0):
        self.server = server
        self.topic = topic
        self.partition = partition

        self.consumer = None
        is_connected = False
        repeat = 20
        while not is_connected and repeat > 0:
            try:
                if if_partition:
                    self.consumer = KafkaConsumer(bootstrap_servers=self.server, value_deserializer=lambda v: json.loads(v))
                    self.consumer.assign([TopicPartition(self.topic, self.partition)])
                else:
                    self.consumer = KafkaConsumer(bootstrap_servers=self.server, value_deserializer=lambda v: json.loads(v))
                    self.consumer.subscribe([self.topic])
                is_connected = True
            except:
                repeat -= 1
                print("Connection failed, retrying...")

class Producer:
    def __init__(self, server, topic):
        self.server = server
        self.topic = topic

        self.producer = None
        is_connected = False
        repeat = 20
        while not is_connected and repeat > 0:
            try:
                self.producer = KafkaProducer(bootstrap_servers=self.server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
                is_connected = True
            except:
                repeat -= 1
                print("Connection failed, retrying...")