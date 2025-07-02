from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg

# Step 1: Create SparkSession
spark = SparkSession.builder \
    .appName("TouristEventAnalysis") \
    .getOrCreate()

# Step 2: Read the CSV from HDFS
df = spark.read.option("header", True).csv("hdfs://localhost:9000/tourist/final_merged.csv", inferSchema=True)

# Step 3: Show schema
print("\n📌 Data Schema:")
df.printSchema()

# Step 4: Top 10 cities with most events
print("\n🏙️ Top Cities by Event Count:")
df.groupBy("city") \
  .agg(count("name").alias("event_count")) \
  .orderBy(col("event_count").desc()) \
  .show(10)

# Step 5: Cities with highest average temperature
print("\n🌡️ Top Cities by Avg Temperature:")
df.groupBy("city") \
  .agg(avg("temperature").alias("avg_temp")) \
  .orderBy(col("avg_temp").desc()) \
  .show(10)

# Step 6: Events during rainy/cloudy/overcast conditions
print("\n🌧️ Events in Rainy/Cloudy/Overcast Weather:")
df.filter(col("description").rlike("(?i)Rain|Cloud|Overcast")) \
  .select("name", "date", "city", "temperature", "description") \
  .show(truncate=False)

# ✅ Done
# Save event count
df.groupBy("city").agg(count("name").alias("event_count")) \
  .orderBy(col("event_count").desc()) \
  .write.mode("overwrite").csv("hdfs://localhost:9000/tourist/output_event_count")

# Save average temperature
df.groupBy("city").agg(avg("temperature").alias("avg_temp")) \
  .orderBy(col("avg_temp").desc()) \
  .write.mode("overwrite").csv("hdfs://localhost:9000/tourist/output_avg_temp")

# Save rainy/cloudy events
df.filter(col("description").rlike("(?i)Rain|Cloud|Overcast")) \
  .write.mode("overwrite").csv("hdfs://localhost:9000/tourist/output_rainy_events")

spark.stop()
