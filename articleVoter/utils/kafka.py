from kafka import KafkaConsumer, KafkaProducer

from django.conf import settings

import json


kafka_config = settings.KAFKA_CONFIG

def json_serializer(data):
    return json.dumps(data).encode('utf-8')


def produce_json_to_kafka(json_data):
    producer = KafkaProducer(
        bootstrap_servers=kafka_config.get('URL'),
        value_serializer=json_serializer,
    )

    producer.send(kafka_config.get('TOPIC'), json_data)
    producer.flush()


def kafka_consumer():
    consumer = KafkaConsumer(
        kafka_config.get('TOPIC'),
        group_id=kafka_config.get('GROUP_ID'),
        bootstrap_servers=kafka_config.get('URL'),  # Adjust if needed
        auto_offset_reset='earliest',
        consumer_timeout_ms=kafka_config.get('TIME_OUT')
    )
    return consumer
