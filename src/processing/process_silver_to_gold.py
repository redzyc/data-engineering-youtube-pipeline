from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import *

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
def process_silver_to_gold():
    spark = create_spark_session()
    silver_data_path = "s3a://youtube-silver/videos_parquet"

    #1 Exctract
    try:
        df_silver = spark.read.option("multiline", "true").parquet(silver_data_path)
    except Exception as e:
        print(f"Error reading silver data: {e}")
        spark.stop()
        return
    if df_silver.rdd.isEmpty():
        print("No silver data found to process.")
        spark.stop()
        return
    
    #2 Transform
    df_gold = df_silver.groupBy("channel_title").agg(
        sum("view_count").alias("total_views"),
        avg("like_count").alias("avg_likes"),
        count("video_id").alias("video_count")
    ).withColumn("last_update", current_timestamp())

    df_gold = df_gold.orderBy(desc("total_views"))
    df_gold.show(5)
   
    #3 Load
    jdbc_url = "jdbc:postgresql://postgres:5432/youtube_analytics"
    df_gold.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "analytics.channel_stats") \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .options(driver="org.postgresql.Driver") \
    .mode("overwrite") \
    .save()
    spark.stop()    
    
    

if __name__ == "__main__":
    process_silver_to_gold()