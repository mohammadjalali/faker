import datetime
import json
import logging
import os

from confluent_kafka import Consumer, KafkaException
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

KAFKA_BROKER_URL = os.environ["KAFKA_BROKER_URL"]
KAFKA_BROKER_PORT = os.environ["KAFKA_BROKER_PORT"]
ELASTICSEARCH_URL = os.environ["ELASTICSEARCH_URL"]
ELASTICSEARCH_PORT = os.environ["ELASTICSEARCH_PORT"]
ELASTICSEARCH_INDEX = os.environ["ELASTICSEARCH_INDEX"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
FAKER_API_URL = "https://fakerapi.it/api/v2/texts?_quantity=100&_locale=fa_IR"
GROUP_ID = "book-consumer-group"
ELASTICSEARCH_HOST = "{}:{}".format(ELASTICSEARCH_URL, ELASTICSEARCH_PORT)

elasticsearch = Elasticsearch([ELASTICSEARCH_HOST])


consumer = Consumer(
    {
        "bootstrap.servers": "{}:{}".format(KAFKA_BROKER_URL, KAFKA_BROKER_PORT),
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe([KAFKA_TOPIC])


def consume_and_store():
    create_index_if_not_exists()
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    break

            message = json.loads(msg.value().decode("utf-8"))

            store_in_elasticsearch(normalize_message(message))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


def create_index_if_not_exists():
    mappings = {
        "properties": {
            "name": {"type": "text"},
            "username": {"type": "keyword"},
            "category": {"type": "keyword"},
            "text": {"type": "text"},
            "inserted_at": {"type": "date"},
        }
    }
    if not elasticsearch.indices.exists(index=ELASTICSEARCH_INDEX):
        elasticsearch.indices.create(index=ELASTICSEARCH_INDEX, mappings=mappings)


def normalize_message(message):
    return {
        "name": message["title"],
        "username": message["author"],
        "category": message["genre"],
        "text": message["content"],
        "inserted_at": datetime.datetime.now().isoformat(),
    }


def store_in_elasticsearch(message):
    try:
        elasticsearch.index(index=ELASTICSEARCH_INDEX, body=message)
        logger.info(f"Indexed document with username: {message['username']}")
    except Exception as e:
        logger.error(f"Error indexing document: {e}")


if __name__ == "__main__":
    consume_and_store()
