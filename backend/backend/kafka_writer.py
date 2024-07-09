from kafka import KafkaProducer
from backend.settings import KAFKA
import json
import logging
from datetime import date, datetime

host = KAFKA.get("HOST")
port = KAFKA.get("PORT")
topic = KAFKA.get("TOPIC")
producer = KafkaProducer(bootstrap_servers=f"{host}:{port}", api_version=(0,10))

logger = logging.getLogger(__name__)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def stream_event(event: dict):
    logger.info('streaming event to kafka')
    producer.send(
        topic,
        # key=event["client_id"].encode("utf-8"),
        value=json.dumps(event, default=json_serial).encode("utf-8")
        )
    # producer.flush()

def create_topic():
    from kafka.admin import KafkaAdminClient, NewTopic
    admin_client = KafkaAdminClient(
        bootstrap_servers=f"{host}:{port}", 
        client_id='test',
        api_version=(0,10)
    )

    if topic not in admin_client.list_topics():
        logger.info('Creating kafka topic')
        topic_list = []
        topic_list.append(NewTopic(name=topic, num_partitions=3, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    else:
        logger.info('Kafka topic already exists.')

create_topic()