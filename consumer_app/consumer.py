import json
import sys
import time
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'user_orders'
ELASTICSEARCH_HOST = 'http://localhost:9200'
ES_INDEX = 'ecommerce_orders'

try:
    print("Initializing Kafka Consumer...")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='order_processing_group'
    )
    
    print("Connecting to Elasticsearch...")
    # Updated syntax for newer elasticsearch-py versions
    es = Elasticsearch(ELASTICSEARCH_HOST)
    
    # Let's get the actual cluster info to prove it connects
    info = es.info()
    print(f"✅ Connected to Elasticsearch (Version: {info['version']['number']})")
    print(f"🎧 Listening to Kafka topic '{KAFKA_TOPIC}'...")

    for message in consumer:
        order_data = message.value
        doc_id = str(order_data.get('order_id')) if order_data.get('order_id') is not None else None
        
        response = es.index(index=ES_INDEX, id=doc_id, document=order_data)
        print(f"Indexed order -> ES Index: {ES_INDEX}, ID: {doc_id}, Result: {response['result']}")

except KeyboardInterrupt:
    print("\nStopping consumer app...")
    consumer.close()
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error Details: {str(e)}")
    sys.exit(1)
