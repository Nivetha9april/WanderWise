from kafka import KafkaConsumer
for msg in KafkaConsumer('tourist_topic', bootstrap_servers='localhost:9092'):
    print(msg.value)
