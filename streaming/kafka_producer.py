from kafka import KafkaProducer
import json
import time
import pandas as pd

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

df = pd.read_csv(r"/home/nivetha-g/Tourist application/data/final_merged.csv")

for _, row in df.iterrows():
    message = row.to_dict()
    producer.send("tourist-events", value=message)
    print("Sent:", message)
    time.sleep(1)  # simulate streaming
