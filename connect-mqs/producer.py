from confluent_kafka import Producer


p = Producer(
    {
        # Configuration: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        'bootstrap.servers': '192.168.0.251:9092,192.168.0.229:9092,192.168.0.240:9092',
        'security.protocol': 'plaintext',
        'sasl.username': 'sasl-username',
        'sasl.password': 'sasl-password',
        'ssl.ca.location': '/location/of/ca'  # ca certificate location
    }
)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for data in ["{'hello': 'world'}"]:
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce('mytopic', data.encode('utf-8'), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()