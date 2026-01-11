import json

from confluent_kafka import Consumer

from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, KAFKA_TOPIC_NAME


def create_kafka_consumer(group_id):
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'latest'
    }

    try:
        consumer = Consumer(conf)
        consumer.subscribe([KAFKA_TOPIC_NAME])
        print(f'Connected to {KAFKA_TOPIC_NAME} (Group {group_id})')
        return consumer
    except Exception as e:
        print(f"Failed to create consumer: {e}")
        return None

def parse_message(msg):
    if msg is None or msg.error():
        return None
    try:
        return json.loads(msg.value().decode('utf-8'))
    except Exception as e:
        print(f"Failed to parse message: {e}")
        return None