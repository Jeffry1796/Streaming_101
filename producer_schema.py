from confluent_kafka import Producer
import random

class ProducerClass:
    def __init__(self):
        producer_conf = {
            'bootstrap.servers': 'localhost:9092'
        }        
        self.producer = Producer(producer_conf)

    def generate_fake_data(self, faker):
        return {
            'transactionId': faker.uuid4(),
            # 'memoId': faker.uuid4(),
            # 'SKU': random.randint(10000, 99999),
            'userId': faker.name(),
            'timestamp': faker.date_time_this_month().isoformat(),
            'amount': round(random.randint(10, 1000),2),
            'currency': random.choice(['USD', 'EUR', 'GBP']),
            'city': faker.city(),
            'country': faker.country(),
            'merchantName': faker.company(),
            'paymentMethod': random.choice(['Debit', 'Credit', 'Online']),
            'ipAddress': faker.ipv4(),
            'voucherCode': random.choice(['DISC10', 'DISC20', 'DISC30']),
            'affiliateId': faker.uuid4()
        }
    
    def produce(self, topic, value, key=None):
        self.producer.produce(
            topic=topic,
            key=key,
            value=value,
            callback=self.delivery_report
        )

    def flush(self, timeout=5):
        self.producer.flush(timeout)

    def delivery_report(self, err, msg):
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            print("Message produced: {}".format(msg.value()))