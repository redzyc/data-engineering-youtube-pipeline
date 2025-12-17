/opt/spark/bin/spark-submit  \
      --master spark://spark-master:7077 \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
      --jars /opt/spark/jars-custom/postgresql-42.7.8.jar \
      --driver-class-path /opt/spark/jars-custom/postgresql-42.7.8.jar \
      --conf spark.cores.max=2 \
      /opt/spark/jobs/process_streaming.py