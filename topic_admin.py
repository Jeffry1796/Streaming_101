from confluent_kafka.admin import AdminClient, NewTopic

class Admin:
    def __init__(self, kafka_broker):
        self.kafka_broker = kafka_broker
        self.admin_client = AdminClient({'bootstrap.servers': kafka_broker})

    def check_topic_exists(self):
        metadata = self.admin_client.list_topics(timeout=5)
        return metadata.topics
    
    def create_topic(self, topic_name, num_partitions, replication_factor):
        list_topics = self.check_topic_exists()
        if topic_name not in list_topics:
            new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
            fs = self.admin_client.create_topics([new_topic])
            for topic, f in fs.items():
                try:
                    f.result()
                    print(f"Topic '{topic}' created successfully.")
                except Exception as e:
                    print(f"Failed to create topic '{topic}': {e}")
        else:
            print(f"Topic '{topic_name}' exists.")