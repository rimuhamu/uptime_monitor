import requests
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import create_kafka_consumer, parse_message
from config import DISCORD_WEBHOOK_URL, KAFKA_GROUP_ID


def get_alert_theme(status):
    if status == 0:
        return "🚫 CONNECTION FAILURE", 15158332  # Red
    elif 500 <= status <= 599:
        return f"🔥 SERVER DOWN: ({status}) Error", 15158332  # Red
    elif 400 <= status <= 499:
        return f"⚠️ CONFIG ISSUE: ({status}) Not Found", 16776960  # Yellow
    else:
        return f"ℹ️ STATUS UPDATE: ({status})", 3447003  # Blue

def send_discord_alert(data):
    readable_time = datetime.fromtimestamp(data['timestamp']).strftime('%d-%m-%Y %H:%M:%S')
    url_val = str(data.get('url', 'Unknown'))
    latency_val = str(data.get('latency', '0'))
    error_val = str(data.get('error') or 'None')
    status_val = data['status_code']
    display_status = "UNREACHABLE" if status_val == 0 else str(status_val)

    title, color = get_alert_theme(status_val)

    embed_content = {
        "title": title,
        "description": f"The monitor detected a failure.",
        "color": color,
        "fields": [
            {"name": "Target URL", "value": url_val, "inline": False},
            {"name": "Status Code", "value": display_status, "inline": True},
            {"name": "Latency", "value": latency_val, "inline": False},
            {"name": "Error Message", "value": error_val, "inline": True},
            {"name": "Timestamp", "value": readable_time, "inline": False},
        ]
    }

    payload = {
        "username": "Uptime Bot",
        "embeds": [embed_content]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Discord alert sent successfully")
        else:
            print(f"Failed to send Discord alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending alert: {e}")

def main():
    group_id = os.getenv('KAFKA_GROUP_ID', 'alert_consumer_group')

    consumer = create_kafka_consumer(group_id=group_id)

    if not consumer: return

    try:
        while True:
            msg = consumer.poll(1.0)

            data = parse_message(msg)

            if data is None:
                continue

            status_code = data.get('status_code')
            url = data.get('url')

            is_down = (status_code == 0 or status_code >= 400)
            if is_down:
                print(f"ALERT: {url} (Status code: {status_code})")
                send_discord_alert(data)
            else:
                print(f"OK: {url} (Status code: {status_code})")

    except KeyboardInterrupt:
        print("Shutting down consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()