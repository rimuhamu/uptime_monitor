import requests
from datetime import datetime
from confluent_kafka import Consumer
import os
import json
from dotenv import load_dotenv

load_dotenv()

def send_discord_alert(data):
    readable_time = datetime.fromtimestamp(data['timestamp']).strftime('%d-%m-%Y %H:%M:%S')
    embed_content = {
        "title": "🔥 WEBSITE DOWN ALERT 🔥",
        "description": f"The monitor detected a failure.",
        "color": 15158332,
        "fields": [
            {"name": "Target URL", "value": data['url'], "inline": False},
            {"name": "Status Code", "value": data['status_code'], "inline": False},
            {"name": "Latency", "value": data['latency'], "inline": False},
            {"name": "Error Message", "value": data['error'], "inline": True},
            {"name": "Timestamp", "value": readable_time, "inline": False},
        ]
    }

    payload = {
        "username": "Uptime Bot",
        "embeds": [embed_content]
    }

    try:
        response = requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json=payload)
        if response.status_code == 204:
            print("Discord alert sent successfully")
        else:
            print(f"Failed to send Discord alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending alert: {e}")

def main():
    conf = {'bootstrap.servers':os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            'group.id': os.getenv('KAFKA_GROUP_ID'),
            'auto.offset.reset': 'latest',
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
            if data['status_code'] != 200:
                print(f"CRITICAL: {data['url']} is DOWN with status {data['status_code']}!")
                send_discord_alert(data)
            else:
                print(f"OK: {data['url']} is UP with status {data['status_code']}!")

    finally:
        consumer.close()

if __name__ == "__main__":
    main()