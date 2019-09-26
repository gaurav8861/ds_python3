from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = ['localhost:9092']


def polls(topic):
    # Initialize consumer Instance
    print("Started polling from kafka bus from topic {0}".format(topic))
    consumer = KafkaConsumer(topic, bootstrap_servers=BOOTSTRAP_SERVERS)

    print("About to start polling for topic:", topic)
    consumer.poll(timeout_ms=6000)
    print("Started Polling for topic:", topic)
    for msg in consumer:
        print("Entered the loop\nKey: ", msg.key, " Value:", msg.value)


