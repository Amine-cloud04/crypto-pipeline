# Real-Time E-Commerce Crypto Analytics Pipeline 🚀

A high-performance data engineering pipeline that ingests live cryptocurrency prices via a Python Producer, processes them through a Spark Structured Streaming engine, and visualizes market trends in real-time using Elasticsearch and Grafana.


## 🛠️ Tech Stack
* **Ingestion:** Python (CoinCap API)
* **Stream Processing:** Apache Kafka & Zookeeper
* **Distributed Compute:** Apache Spark (Structured Streaming)
* **Storage:** Elasticsearch
* **Visualization:** Grafana & Kibana
* **Environment:** Docker & GitHub Codespaces

## 🏗️ System Architecture
1.  **Producer:** Fetches live Bitcoin/Ethereum prices and pushes JSON events to the `user_orders` Kafka topic.
2.  **Consumer (Spark):** Reads the stream, joins it with static product metadata (`products.csv`), and performs real-time schema validation.
3.  **Sink:** Data is indexed into Elasticsearch with explicit date-mapping for time-series integrity.
4.  **Dashboard:** Grafana monitors `live_price` volatility with sub-5s latency.

## 🚀 Getting Started

### 1. Launch Infrastructure
```bash
docker compose down -v
docker compose up -d
# Wait 30 seconds for Kafka & ES to stabilize
2. Initialize Elasticsearch Schema (Critical)
Run this to ensure the order_date is recognized as a time-series field:

Bash
curl -X PUT "localhost:9200/crypto_live_final" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "order_date": { "type": "date" },
      "live_price": { "type": "double" },
      "product_id": { "type": "keyword" }
    }
  }
}'
3. Start the Pipeline
Open two terminals:

Terminal A (Producer): python3 data/producer.py

Terminal B (Consumer): sbt "runMain pipeline.StreamingConsumer"

4. Access Dashboards
Grafana: http://localhost:3000 (User: admin / Pass: admin)

Kibana: http://localhost:5601

🔧 Troubleshooting
KafkaTimeoutError: Ensure Docker containers are running and 127.0.0.1 is used instead of localhost in the producer.

Offset Out of Range: Delete the checkpoint folder: rm -rf /tmp/spark-checkpoints-crypto.

No Data in Grafana: Ensure the Time Range is set to Last 5 Minutes and the time field is mapped to order_date.

 INPT 2026
