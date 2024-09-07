from pyspark.sql import SparkSession
import time

# Create Spark session
spark = SparkSession.builder.appName("LongRunningJob").getOrCreate()

# Create a DataFrame
df = spark.createDataFrame([(i, i * 2) for i in range(1000000)], ["num", "double_num"])

# Perform a transformation and action that takes time
df_filtered = df.filter(df.num % 2 == 0)
df_filtered_count = df_filtered.count()

print(f"Count of even numbers: {df_filtered_count}")

# Introduce a delay to keep the job running longer
time.sleep(600)  # Sleep for 10 minutes

# Stop the Spark session
spark.stop()
