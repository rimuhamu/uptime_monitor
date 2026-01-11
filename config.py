import os

from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC_NAME = os.getenv('KAFKA_TOPIC_NAME')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID')
SITES_TO_MONITOR = os.getenv('SITES_TO_MONITOR')
SLEEP_TIME = os.getenv('SLEEP_TIME')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')