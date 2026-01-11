from confluent_kafka import Producer
import json
import requests
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import KAFKA_BOOTSTRAP_SERVERS, SITES_TO_MONITOR, KAFKA_TOPIC_NAME, SLEEP_TIME


def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivery succeeded: {}'.format(msg.topic()))


def get_website_status(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "url": url,
            "status_code": response.status_code,
            "latency": round(response.elapsed.total_seconds(), 3),
            "timestamp": time.time(),
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status_code": 0,
            "latency": 0,
            "error": str(type(e).__name__),
            "timestamp": time.time()
        }
def main():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    }

    producer = Producer(conf)
    try:
        while True:
            for url in SITES_TO_MONITOR.split(','):
                data = get_website_status(url)
                serialized_data = json_serializer(data)
                producer.produce(KAFKA_TOPIC_NAME, value=serialized_data, callback=delivery_report)

            producer.flush()
            time.sleep(int(SLEEP_TIME))
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        producer.flush()

if __name__ == "__main__":
    main()