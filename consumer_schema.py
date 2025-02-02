from confluent_kafka import Consumer

class ConsumerClass:
    def __init__(self):
        consumer_conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'transaction_group',
            'auto.offset.reset': 'earliest',
        }

        self.consumer = Consumer(consumer_conf)
    
    def subscribe(self, topics):
        self.consumer.subscribe([topics])