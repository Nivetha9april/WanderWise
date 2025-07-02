from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, desc

# Initialize Spark session
spark = SparkSession.builder \
    .appName("WanderWise Analytics") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("WARN")

# Read the final enriched CSV from HDFS
data_path = "hdfs:///tourist_data/final.csv"

df = spark.read.option("header", "true").option("inferSchema", "true").csv(data_path)

# ----------------------------
# ✅ 1. Most Frequent Events
# ----------------------------
event_counts = df.groupBy("name").agg(count("*").alias("event_count")) \
    .orderBy(desc("event_count"))

# ----------------------------
# ✅ 2. Most Popular Cities by Event Count
# ----------------------------
city_popularity = df.groupBy("city").agg(count("*").alias("event_count")) \
    .orderBy(desc("event_count"))

# ----------------------------
# ✅ 3. Average Temperature per City
# ----------------------------
city_weather = df.groupBy("city").agg(avg("temperature").alias("avg_temp")) \
    .orderBy(desc("avg_temp"))

# ----------------------------
# ✅ 4. Recommended Places Table
# ----------------------------
recommendation_df = df.select("city", "name", "description", "summary").dropDuplicates()

# ----------------------------
# ✅ Save results to HDFS
# ----------------------------
output_base = "hdfs:///tourist_data/analytics/"

event_counts.write.mode("overwrite").option("header", "true").csv(output_base + "event_counts")
city_popularity.write.mode("overwrite").option("header", "true").csv(output_base + "popular_cities")
city_weather.write.mode("overwrite").option("header", "true").csv(output_base + "city_weather")
recommendation_df.write.mode("overwrite").option("header", "true").csv(output_base + "recommendations")

print("✅ WanderWise analytics job completed and results written to HDFS.")

# Stop Spark
spark.stop()
