# Website Uptime Monitor

A lightweight uptime monitoring system using Kafka for real-time website health checks and Discord notifications.

## Features

- Monitors multiple websites concurrently
- Real-time status checks with latency tracking
- Discord alerts for failures (4xx, 5xx, connection errors)
- Kafka-based event streaming architecture

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Kafka:
```bash
docker-compose up -d
```

3. Configure environment variables in `.env`:
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_NAME=website-monitor
KAFKA_GROUP_ID=monitor-consumer
SITES_TO_MONITOR=https://google.com,https://github.com
SLEEP_TIME=60
DISCORD_WEBHOOK_URL=your_webhook_url
```

## Usage

Run the producer (monitors websites):
```bash
python producer/main.py
```

Run the consumer (sends alerts):
```bash
python consumer/main.py
```

## Testing

```bash
pytest -m pytest
```