from pyspark.sql import SparkSession

# Tạo Spark session
spark = SparkSession.builder.appName("MySparkApp").getOrCreate()

# Đọc dữ liệu từ file CSV
data = spark.read.csv("/home/anhdd/Downloads/VHT_Training_BigData/DataEngineering/StreamProcessing/Spark-Application/data.csv", header=True, inferSchema=True)

# Thực hiện các thao tác
result = data.groupBy("Name").agg({"Score": "sum"})

# Hiển thị kết quả
result.show()

# Dừng Spark session
spark.stop()
