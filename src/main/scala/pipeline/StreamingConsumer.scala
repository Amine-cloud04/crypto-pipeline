package pipeline

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object StreamingConsumer {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("CryptoLiveStream")
      .master("local[*]")
      .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    val schema = new StructType()
      .add("order_id", StringType)
      .add("customer_id", StringType)
      .add("product_id", StringType)
      .add("quantity", DoubleType) // This is our price
      .add("order_date", StringType)
      .add("status", StringType)

    // 1. Read from Kafka
    val rawDF = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "127.0.0.1:9092")
      .option("subscribe", "user_orders")
      .load()

    // 2. Parse JSON
    val jsonDF = rawDF.selectExpr("CAST(value AS STRING)")
      .select(from_json(col("value"), schema).as("data"))
      .select("data.*")

    // 3. Load Metadata (CSV)
    val productsDF = spark.read
      .option("header", "true")
      .csv("data/products.csv")

    // 4. Join & Enrich (This creates enrichedDF)
    val enrichedDF = jsonDF.join(productsDF, Seq("product_id"), "left")
      .withColumn("live_price", col("quantity"))

    // 5. Write to Elasticsearch
    val query = enrichedDF.writeStream
      .outputMode("append")
      .format("org.elasticsearch.spark.sql")
      .option("checkpointLocation", "/tmp/spark-checkpoints-crypto")
      .option("es.resource", "crypto_live_final")
      .option("es.nodes", "localhost")
      .option("es.port", "9200")
      .start()

    println("🚀 Spark Engine Active. Monitoring Kafka for Crypto Events...")
    query.awaitTermination()
  }
}
