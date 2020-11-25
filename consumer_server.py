import time

from confluent_kafka import Consumer, Producer, OFFSET_BEGINNING
from confluent_kafka.admin import AdminClient, NewTopic


BROKER_URL = "PLAINTEXT://localhost:9092"


def consume(topic_name):
    """Consumes data from the Kafka Topic"""
    c = Consumer(
        {
            "bootstrap.servers": BROKER_URL,
            "group.id": "0",
            "auto.offset.reset": "earliest",
        }
    )

    c.subscribe([topic_name], on_assign=on_assign)

    while True:
        message = c.poll(1.0)
        if message is None:
            print("no message received by consumer")
        elif message.error() is not None:
            print(f"error from consumer {message.error()}")
        else:
            print(f"consumed message: {message.value()}")
        time.sleep(0.1)


def on_assign(consumer, partitions):
    """Callback for when topic assignment takes place"""
    # the beginning or earliest
    for partition in partitions:
        partition.offset = OFFSET_BEGINNING

    consumer.assign(partitions)


consume("sf.crime.topic")
