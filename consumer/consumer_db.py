import json
from confluent_kafka import Consumer

from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, KAFKA_TOPIC_NAME, DB_HOST
from database import SessionLocal, init_db, WebsiteStats

def save_to_db(data):
    session = SessionLocal()

    try:
        record = WebsiteStats(
            url=data['url'],
            status_code=data['status_code'],
            latency=data['latency']
        )

        session.add(record)
        session.commit()
        print(f"DB Saved: {data['url']}")

    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        session.close()

def main():
    init_db()

    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'latest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([KAFKA_TOPIC_NAME])

    print("ORM DB Archiver Running...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None: continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            try:
                data = json.loads(msg.value().decode('utf-8'))
                save_to_db(data)
            except Exception as e:
                print(f"Data Error: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    main()