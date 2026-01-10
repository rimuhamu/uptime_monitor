from confluent_kafka import Producer
import json
import requests
import time
import config

conf = {'bootstrap.servers': config.BOOTSTRAP_SERVERS,}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivery succeeded: {}'.format(msg.topic()))

while True:
    for url in config.SITES_TO_MONITOR:
        try:
            status = requests.get(url, timeout=5).status_code
        except:
            status = 500

        payload = json.dumps({'url': url, 'status': status, 'time': time.time()})
        producer.produce('website_health', value=payload.encode('utf-8'), callback=delivery_report)

    producer.flush()
    time.sleep(10)