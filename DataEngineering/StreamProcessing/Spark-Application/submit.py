import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType
sc = SparkContext.getOrCreate(SparkConf().setMaster('spark://localhost:7077'))
sc.setLogLevel("INFO")
spark = SparkSession.builder.getOrCreate()

# Create a simple DataFrame
data = [("Alice", 1), ("Bob", 2)]
columns = ["Name", "Id"]

df = spark.createDataFrame(data, columns)
df.show()

# Stop SparkSession
spark.stop()
