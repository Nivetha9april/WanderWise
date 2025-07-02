from pyspark.sql import SparkSession

# Start SparkSession with Hive support
spark = SparkSession.builder \
    .appName("TouristHiveApp") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
    .enableHiveSupport() \
    .getOrCreate()

# Show all databases
spark.sql("SHOW DATABASES").show()

# Use your database
spark.sql("USE tourist_db")

# Read the Hive table
df = spark.sql("SELECT * FROM tourist_events")

# Show data
df.show(10)

# Save it as a DataFrame for use in Streamlit
df.toPandas().to_csv("data/tourist_events.csv", index=False)
