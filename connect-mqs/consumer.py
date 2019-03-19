from confluent_kafka import Consumer, KafkaError


c = Consumer({
    # Configuration: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    'bootstrap.servers': '192.168.0.251:9092,192.168.0.229:9092,192.168.0.240:9092',
    'security.protocol': 'plaintext',
    'sasl.username': 'sasl-username',
    'sasl.password': 'sasl-password',
    'ssl.ca.location': '/location/of/ca',  # ca certificate location   
    'group.id': 'mygroup',  # this is the comsumer group
    'auto.offset.reset': 'earliest'
})

c.subscribe(['mytopic'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if not msg.error():
        print('Received message: {}'.format(msg.value().decode('utf-8')))
    elif msg.error().code() == KafkaError._PARTITION_EOF:
        print("Consumer error: reached the broker EOF")
    else:
        print("Consumer error: {}".format(msg.error()))

c.close()