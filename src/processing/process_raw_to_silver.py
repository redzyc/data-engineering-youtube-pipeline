from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import *
from pyspark.sql.types import *

def create_spark_session():
    spark = SparkSession.builder \
        .appName("RawToSilverProcessing") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
    return spark
def process_data():
    spark = create_spark_session()

    raw_data_path = "s3a://youtube-raw/*.json"
    silver_data_path = "s3a://youtube-silver/videos_parquet"


    #1 Exctract
    try:
        df_raw = spark.read.option("multiline", "true").json(raw_data_path)
    except Exception as e:
        print(f"Error reading raw data: {e}")
        spark.stop()
        return
    if df_raw.rdd.isEmpty():
        print("No raw data found to process.")
        spark.stop()
        return
    
    #2 Transform
    df_silver = df_raw.select(
        col("id").alias("video_id"),
        col("snippet.title").alias("title"),
        col("snippet.channelTitle").alias("channel_title"),
        col("statistics.viewCount").cast(LongType()).alias("view_count"),
        col("statistics.likeCount").cast(LongType()).alias("like_count"),
        col("statistics.commentCount").cast(LongType()).alias("comment_count"),
        col("snippet.publishedAt").alias("published_at_str")
    )
    df_silver = df_silver \
        .withColumn("published_at", to_timestamp(col("published_at_str"))) \
        .drop("published_at_str") \
        .withColumn("ingestion_timestamp", current_timestamp()) \
        .dropDuplicates(["video_id"]) \
        .fillna(0, subset=["view_count", "like_count", "comment_count"])
    
    df_silver.show(5)
   
    #3 Load
    df_silver.write \
    .mode("append") \
    .partitionBy("channel_title") \
    .parquet(silver_data_path) 
    spark.stop()

if __name__ == "__main__":
    process_data()