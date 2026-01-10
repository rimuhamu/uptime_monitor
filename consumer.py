from confluent_kafka import Consumer
import os
import json
from dotenv import load_dotenv

load_dotenv()

conf = {'bootstrap.servers':os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        'group.id': os.getenv('KAFKA_GROUP_ID'),
        'auto.offset.reset': 'earliest',
        }

consumer = Consumer(conf)
consumer.subscribe([os.getenv('KAFKA_TOPIC_NAME')])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None: continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        data = json.loads(msg.value().decode('utf-8'))
        if data['status'] >= 400:
            print(f"CRITICAL: {data['url']} is DOWN with status {data['status']}!")
        else:
            print(f"OK: {data['url']} is UP with status {data['status']}!")

finally:
    consumer.close()