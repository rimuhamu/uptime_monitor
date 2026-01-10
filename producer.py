from confluent_kafka import Producer
import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()

conf = {'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivery succeeded: {}'.format(msg.topic()))

while True:
    for url in os.getenv('SITES_TO_MONITOR').split(','):
        try:
            status = requests.get(url, timeout=5).status_code
        except:
            status = 500

        payload = json.dumps({'url': url, 'status': status, 'time': time.time()})
        producer.produce(os.getenv('KAFKA_TOPIC_NAME'), value=payload.encode('utf-8'), callback=delivery_report)

    producer.flush()
    time.sleep(10)