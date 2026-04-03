import json
import time
import datetime
import random
import pandas as pd
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    api_version=(0, 10, 1),
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

df_orders = pd.read_csv('data/orders.csv')
templates = df_orders.to_dict(orient='records')

print("🚀 Starting Clean Stream with ISO dates...")

try:
    while True:
        order = random.choice(templates).copy()
        # 🔥 Using isoformat() adds the 'T' and removes the space
        order['order_date'] = datetime.datetime.now().isoformat()
        
        producer.send('user_orders', value=order)
        print(f"📡 Sent Order {order['order_id']} | {order['order_date']}")
        time.sleep(1.5) 
except:
    pass
finally:
    producer.flush()
