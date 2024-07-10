from kafka import KafkaConsumer
import json
import os
from models import Event, EventProperty, UserProperty
from sqlalchemy.orm import Session
from db import engine
import logging

logger = logging.getLogger(__name__)

host = os.environ.get("KAFKA_HOST")
port = os.environ.get("KAFKA_PORT")
topic = os.environ.get("KAFKA_TOPIC")


def check_topics():
    consumer = KafkaConsumer(
        topic, bootstrap_servers=f"{host}:{port}", api_version=(0, 10)
    )

    topics = consumer.topics()
    if not topics:
        msg = "No Kafka topics found. Broker may be unavailable"
        logger.warning(msg)
        print(msg)
    else:
        msg = f"Kafka topics found: {topics}"
        logger.info(msg)
        print(msg)
    consumer.close()


def processMessage(message: dict):
    try:
        data = json.loads(message.value.decode("utf-8"))
        client_id = data["client_id"]
        user_id = data["user_id"]
        with Session(engine) as session:
            for event in data.get("events", []):
                event_record = Event(
                    client_id=client_id,
                    user_id=user_id,
                    name=event["event"],
                    created_at=event["created_at"],
                )
                session.add(event_record)
                for prop in event.get("properties", []):
                    event_prop_record = EventProperty(
                        name=prop["name"], value=prop["value"], event=event_record
                    )
                    session.add(event_prop_record)
            for property in data.get("properties", []):
                property_record = UserProperty(
                    client_id=client_id,
                    user_id=user_id,
                    name=property["name"],
                    value=property["value"],
                )
                session.add(property_record)
            session.commit()
    except Exception as ex:
        print(f"Failed to process message: {str(ex)}. Payload {str(message)}")


def consume():
    print("Start consuming messages from Kafka...")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=f"{host}:{port}",
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="consumer",
        api_version=(0, 10),
    )

    for message in consumer:
        print("New message received. Processing...")
        processMessage(message)
    consumer.close()


if __name__ == "__main__":
    print("Staring consumer...")
    check_topics()
    consume()
