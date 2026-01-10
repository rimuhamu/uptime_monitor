from confluent_kafka import Producer
import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()

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
            "timestamp": time.time()
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status_code": 503, # Service unavailable
            "latency": 0,
            "error": str(e),
            "timestamp": time.time()
        }
def main():
    conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    }

    producer = Producer(conf)

    while True:
        for url in os.getenv('SITES_TO_MONITOR').split(','):
            data = get_website_status(url)
            serialized_data = json_serializer(data)
            producer.produce(os.getenv('KAFKA_TOPIC_NAME'), value=serialized_data, callback=delivery_report)

        producer.flush()
        time.sleep(int(os.getenv('SLEEP_TIME')))

if __name__ == "__main__":
    main()