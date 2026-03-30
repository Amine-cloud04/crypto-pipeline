<<<<<<< HEAD
import pandas as pd\nfrom kafka import KafkaProducer\nimport json\n\nclass CSVtoKafkaProducer:\n    def __init__(self, kafka_servers):\n        self.producer = KafkaProducer(\n            bootstrap_servers=kafka_servers,\n            value_serializer=lambda v: json.dumps(v).encode('utf-8')\n        )\n\n    def produce_from_csv(self, csv_file, topic):\n        df = pd.read_csv(csv_file)\n        for index, row in df.iterrows():\n            self.producer.send(topic, row.to_dict())\n            print(f'Sent row {index} to topic {topic}')\n        self.producer.flush()\n        print('Finished sending all rows.')\n\nif __name__ == '__main__':\n    kafka_servers = 'localhost:9092'  # Change this to your Kafka server address\n    topic_name = 'your_topic_name'  # Replace with your topic name\n    csv_file_path = 'path/to/your/file.csv'  # Replace with the path to your CSV file\n    producer = CSVtoKafkaProducer(kafka_servers)\n    producer.produce_from_csv(csv_file_path, topic_name)
=======
import pandas as pd
from kafka import KafkaProducer
import json
import time

class CSVtoKafkaProducer:
    def __init__(self, kafka_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce_from_csv(self, csv_file, topic):
        df = pd.read_csv(csv_file)
        print(f"Starting to stream {len(df)} records to Kafka topic: {topic}")
        
        for index, row in df.iterrows():
            record = row.to_dict()
            self.producer.send(topic, record)
            print(f'Sent order_id {record.get("order_id", index)} to Kafka')
            time.sleep(0.5) # Slight delay to simulate real-time streaming
            
        self.producer.flush()
        print('Finished streaming all rows.')

if __name__ == '__main__':
    kafka_servers = 'localhost:9092'
    topic_name = 'user_orders' 
    csv_file_path = 'data/orders.csv'
    
    producer = CSVtoKafkaProducer(kafka_servers)
    producer.produce_from_csv(csv_file_path, topic_name)
>>>>>>> 12ab2a9 (Migration to Real-Time Streaming: Kafka, Spark, and Elasticsearch integrated)
