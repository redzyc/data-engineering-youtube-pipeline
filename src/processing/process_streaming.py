from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


json_schema = StructType([
    StructField("id", StringType(), True),
    StructField("snippet", StructType([
        StructField("title", StringType(), True),
        StructField("channelTitle", StringType(), True),
        StructField("publishedAt", StringType(), True)
    ]), True),
    StructField("statistics", StructType([
        StructField("viewCount", StringType(), True), 
        StructField("likeCount", StringType(), True),
        StructField("commentCount", StringType(), True)
    ]), True)
])
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/youtube_analytics") \
    .option("dbtable", "speed_layer.realtime_stats") \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .options(driver="org.postgresql.Driver") \
    .mode("append") \
    .save()
def process_streaming_data():
    spark = SparkSession.builder \
        .appName("YouTubeStreamingProcessor") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()
    #1 Extract
    df_kafka_raw = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "youtube_raw") \
        .option("startingOffsets", "latest") \
        .load()
    

    df_parsed = df_kafka_raw.selectExpr("CAST(value AS STRING) as json_string") \
        .select(from_json(col("json_string"), json_schema).alias("data")) \
        .select("data.*")
    

    #2 Transform
    df_clean = df_parsed.select(
        col("id").alias("video_id"),
        col("snippet.title").alias("title"),
        col("snippet.channelTitle").alias("channel_title"),
        col("statistics.viewCount").cast("long").alias("view_count"),
        col("statistics.likeCount").cast("long").alias("like_count"),
        col("statistics.commentCount").cast("long").alias("comment_count"),
        current_timestamp().alias("processing_time")
    ).filter(col('video_id').isNotNull()) \
     .fillna(0, subset=["view_count", "like_count", "comment_count"])

    windowed_counts = df_clean \
        .withWatermark("processing_time", "10 minute") \
        .groupBy(
            window(col("processing_time"), "1 minute"),
            col("video_id"),     
            col("title"),         
            col("channel_title") 
        ).agg(
            sum("view_count").alias("total_views"),
            sum("like_count").alias("total_likes"),       
            sum("comment_count").alias("total_comments") 
        ).select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("video_id"),
            col("title"),
            col("channel_title"),
            col("total_views"),
            col("total_likes"),
            col("total_comments")
        )
    
    #3 Load

    query = windowed_counts.writeStream \
        .outputMode("update") \
        .foreachBatch(write_to_postgres) \
        .trigger(processingTime="10 seconds") \
        .start()
    

    query.awaitTermination()

if __name__ == "__main__":
    process_streaming_data()