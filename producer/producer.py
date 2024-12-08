import json
import logging
import os
import time

import requests
from confluent_kafka import Producer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

KAFKA_BROKER_URL = os.environ["KAFKA_BROKER_URL"]
KAFKA_BROKER_PORT = os.environ["KAFKA_BROKER_PORT"]
TOPIC_NAME = "faker-data"
FAKER_API_URL = "https://fakerapi.it/api/v2/texts?_quantity=100&_locale=fa_IR"


producer = Producer(
    {"bootstrap.servers": "{}:{}".format(KAFKA_BROKER_URL, KAFKA_BROKER_PORT)}
)


def produce():
    while True:
        data = fetch_data_from_fakerapi()
        if data:
            produce_to_kafka(data)
        time.sleep(60)


def fetch_data_from_fakerapi():
    try:
        response = requests.get(FAKER_API_URL)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            logger.error("Failed to fetch data: {}".format(producer.poll(0)))
            return []
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return []


def produce_to_kafka(data):
    for item in data:
        try:
            producer.produce(TOPIC_NAME, json.dumps(item))
            producer.poll(0)
            logger.info("Produced data {}".format(item))
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {e}")


if __name__ == "__main__":
    produce()
