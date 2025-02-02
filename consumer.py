from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
import consumer_schema as cs

if __name__ == '__main__':
    avro_schema = 'schema.avsc'

    with open(avro_schema, 'r') as f:
        schema_str = f.read()

    consumer = cs.ConsumerClass()

    schema_url = 'http://localhost:8081'
    topic = 'transaction'
    schema_registry_conf = {'url': schema_url}
    schema_url = SchemaRegistryClient(schema_registry_conf)
    avro_deserializer = AvroDeserializer(schema_url, schema_str)
    consumer.subscribe(topic)

    try:
        while True:
            msg = consumer.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            res = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            print(f"Received message: {res}")
    except KeyboardInterrupt:
        consumer.consumer.close()