from kafka import KafkaProducer

from django.conf import settings

import json


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


def produce_json_to_kafka(json_data):
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_URL,
        value_serializer=json_serializer,
    )

    producer.send(settings.KAFKA_TOPIC, json_data)
    producer.flush()
