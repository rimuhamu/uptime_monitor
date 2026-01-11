import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import  KAFKA_GROUP_ID
from database import SessionLocal, init_db, WebsiteStats
from utils import create_kafka_consumer, parse_message


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

    group_id = os.getenv('KAFKA_GROUP_ID', 'db_consumer_group')

    consumer = create_kafka_consumer(group_id=group_id)

    if not consumer: return

    print("ORM DB Archiver Running...")

    try:
        while True:
            msg = consumer.poll(1.0)

            data = parse_message(msg)
            if not data: continue

            save_to_db(data)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    main()