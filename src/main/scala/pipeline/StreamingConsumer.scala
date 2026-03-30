package pipeline

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object StreamingConsumer {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("KafkaToElasticsearch")
      .master("local[*]")
      .config("spark.es.nodes", "localhost")
      .config("spark.es.port", "9200")
      .config("spark.es.nodes.wan.only", "true")
      .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    val orderSchema = new StructType()
      .add("order_id", IntegerType)
      .add("customer_id", DoubleType)
      .add("product_id", IntegerType)
      .add("quantity", DoubleType)
      .add("order_date", StringType)
      .add("status", StringType)

    val kafkaStream = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "user_orders")
      .load()

    val parsedStream = kafkaStream.selectExpr("CAST(value AS STRING) as json_str")
      .withColumn("data", from_json(col("json_str"), orderSchema))
      .select("data.*")
      // SENIOR FIX: Aggressively filter out any record that has a non-finite number (NaN or Infinity)
      // and ensure the order_id is valid before sending to Elasticsearch
      .filter(
        col("order_id").isNotNull && 
        col("quantity").isNotNull && !col("quantity").isNaN &&
        col("customer_id").isNotNull && !col("customer_id").isNaN
      )

    println("🚀 Clean Stream Started. Waiting for Kafka data...")

    val query = parsedStream.writeStream
      .format("org.elasticsearch.spark.sql")
      .outputMode("append")
      .option("checkpointLocation", "/tmp/spark-checkpoints-final-v4")
      .option("es.resource", "spark_ecommerce_orders")
      .option("es.mapping.id", "order_id")
      .start()

    query.awaitTermination()
  }
}
