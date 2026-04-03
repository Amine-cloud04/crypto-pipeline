# Live Crypto Stream: Real-Time Data Engineering Pipeline

A high-performance, event-driven data pipeline that ingests live cryptocurrency trade data via **WebSockets**, processes it in real-time using **Spark Structured Streaming**, and visualizes market volatility in **Kibana**.

## 🏗️ Architecture
The pipeline implements a "Hot Path" architecture for sub-second latency:
1.  **Data Source**: Live market data from the **CoinCap WebSocket API**.
2.  **Ingestion Layer**: **Apache Kafka** serving as a distributed, fault-tolerant message buffer.
3.  **Stream Processing**: **Spark Structured Streaming (Scala)** performing real-time schema enforcement, metadata enrichment (joining with `products.csv`), and data transformation.
4.  **Storage & Indexing**: **Elasticsearch** for high-velocity document indexing and search.
5.  **Visualization**: **Kibana** for real-time time-series dashboards and price monitoring.

### 📊 Project Data Flow

```mermaid
graph LR
    subgraph External
    api[CoinCap WebSocket] -->|Live JSON| producer_py[producer.py]
    end

    subgraph Ingestion
    producer_py -->|1. Produce Events| kafka_topic[Kafka Topic: user_orders]
    end

    subgraph Streaming
    products_csv[(products.csv)] -.->|Metadata Join| spark_consumer
    kafka_topic -->|2. Structured Stream| spark_consumer[Spark Structured Streaming]
    spark_consumer -->|3. Enrich & Validate| clean_stream[Enriched Stream]
    end

    subgraph "ELK Stack"
    clean_stream -->|4. Index Docs| elasticsearch[(Elasticsearch)]
    elasticsearch <-->|5. Live Dashboard| kibana[Kibana]
    end

    style api fill:#f96,stroke:#333;
    style kafka_topic fill:#ccf,stroke:#333;
    style spark_consumer fill:#ff9,stroke:#333;
    style elasticsearch fill:#dfd,stroke:#333;
🛠️ Tech Stack
Languages: Scala 2.12, Python 3.10

Stream Processing: Apache Spark 3.2.4

Messaging: Confluent Kafka 7.4.0

ELK Stack: Elasticsearch & Kibana 7.17.0

Connectivity: WebSockets (CoinCap API)

Containerization: Docker & Docker Compose

🚀 How to Run
1. Initialize Infrastructure
Ensure Docker is running and launch the stack:
```bash
docker compose up -d
```

2. Start the Spark Engine
Compile the Scala application and start the streaming query:
```bash
sbt "runMain pipeline.StreamingConsumer"
```

3. Launch Live Ingestion
Start the Python producer to bridge the external API to Kafka:
```bash
python3 data/producer.py
```

4. Visualize
Kibana: Access `http://localhost:5601`.

Data View: Create a view for `crypto_live_final*` using `order_date` as the timestamp.

Real-Time: Set the refresh interval to 2 seconds to watch live price movements.

🛡️ Key Engineering Features
ISO-8601 Compliance: Enforced strict timestamp serialization to ensure seamless indexing into Elasticsearch date types.

Explicit Schema Enforcement: Utilized StructType in Scala to prevent runtime type-inference errors and ensure data contract stability.

Self-Healing Producer: The Python ingestion layer includes a recursive reconnection loop to handle WebSocket timeouts and network jitter.

Stateless Enrichment: Real-time join between high-velocity Kafka events and static broadcast variables (product metadata).