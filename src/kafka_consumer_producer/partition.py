from kafka.admin import KafkaAdminClient, NewPartitions, NewTopic

if __name__ == '__main__':
    admin_client = KafkaAdminClient(bootstrap_servers='localhost:29092')
    topic_partitions = {}
    topic = "ML"
    new_partitions = NewPartitions(total_count=2)
    new_topic = [NewTopic(name=topic)]
    topic_partitions[topic] = new_partitions
    admin_client.create_topics(new_topic)
    admin_client.create_partitions(topic_partitions)