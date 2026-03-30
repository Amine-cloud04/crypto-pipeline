import pandas as pd
from kafka import KafkaProducer
import json
import time

class CSVtoKafkaProducer:
    def __init__(self, kafka_servers):
        # Initializing the Kafka Producer
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_servers,
            # Serialize dictionary data to JSON format for Kafka
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce_from_csv(self, csv_file, topic):
        # Read the local CSV file
        df = pd.read_csv(csv_file)
        
        # CRITICAL FIX: Replace pandas NaN values with Python None.
        # This ensures the JSON sent to Kafka contains 'null' instead of 'NaN',
        # preventing Spark parsing errors.
        df = df.where(pd.notnull(df), None)
        
        print(f"Starting to stream {len(df)} records to Kafka topic: {topic}")
        
        for index, row in df.iterrows():
            record = row.to_dict()
            
            # Send the record to the Kafka topic
            self.producer.send(topic, record)
            
            print(f'Sent order_id {record.get("order_id", index)} to Kafka')
            
            # Small delay to simulate real-time traffic
            time.sleep(0.5)
            
        # Ensure all messages are sent before finishing
        self.producer.flush()
        print('Finished streaming all rows.')

if __name__ == '__main__':
    # Configuration matches your Docker setup
    kafka_servers = 'localhost:9092'
    topic_name = 'user_orders' 
    csv_file_path = 'data/orders.csv'
    
    producer = CSVtoKafkaProducer(kafka_servers)
    producer.produce_from_csv(csv_file_path, topic_name)