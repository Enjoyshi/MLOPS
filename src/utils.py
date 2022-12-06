from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import TopicPartition
import json
import time

class Consumer:
    def __init__(self, server, topic, if_partition = False, partition = 0):
        self.server = server
        self.topic = topic
        self.partition = partition

        consumer = None
        is_connected = False
        repeat = 20
        while not is_connected and repeat != 0:
            try:
                if if_partition:
                    consumer = KafkaConsumer(bootstrap_servers=self.server, value_deserializer=lambda v: json.loads(v))
                    consumer.assign([TopicPartition(self.topic, self.partition)])
                else:
                    consumer = KafkaConsumer(bootstrap_servers=self.server, value_deserializer=lambda v: json.loads(v))
                    consumer.subscribe([self.topic])
                is_connected = True
            except:
                repeat -= 1
                print("Connection failed on consumer, retrying...")
                time.sleep(2)

        if not is_connected:
            raise Exception("Connection failed on consumer, aborting...")
        else:
            print("Connection established on consumer")
            self.consumer = consumer

class Producer:
    def __init__(self, server, topic):
        self.server = server
        self.topic = topic

        producer = None
        is_connected = False
        repeat = 20
        while not is_connected and repeat != 0:
            try:
                producer = KafkaProducer(bootstrap_servers=self.server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
                is_connected = True
            except:
                repeat -= 1
                print("Connection failed on producer, retrying...")
                #time.sleep(2)

        if not is_connected:
            raise Exception("Connection failed on producer, aborting...")
        else:
            print("Connection established on producer")
            self.producer = producer