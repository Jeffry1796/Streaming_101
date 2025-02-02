from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from topic_admin import Admin
from faker import Faker
import producer_schema as ps
import time

if __name__ == '__main__':
    topic_name = 'transaction'
    kafka_broker = 'localhost:9092'
    admin = Admin(kafka_broker)
    admin.create_topic(topic_name, num_partitions=1, replication_factor=1)

    with open('schema.avsc', 'r') as f:
        schema_str = f.read()

    schema_url = 'http://localhost:8081'
    schema_registry_client = SchemaRegistryClient({'url': schema_url})
    keySerializer = StringSerializer()
    valueSerializer = AvroSerializer(schema_registry_client, schema_str)

    producer = ps.ProducerClass()

    while True:
        try:
            transaction = producer.generate_fake_data(Faker())
            producer.produce(topic = topic_name, key=keySerializer(transaction['transactionId'], SerializationContext(topic_name, MessageField.KEY)), value=valueSerializer(transaction, SerializationContext(topic_name, MessageField.VALUE)))
            producer.flush()
            time.sleep(1)
        except Exception as e:
            print(e)
            print("Failed to produce transaction: {}".format(e))
            break