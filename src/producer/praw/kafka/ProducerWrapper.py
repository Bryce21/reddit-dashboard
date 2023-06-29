import socket
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print(
            "Produced event to topic {topic}".format(topic=msg.topic())
        )


class ProducerWrapper:

    def close_producer(self):
        print("Forcing producer flush on shutdown: ")
        self.producer.flush(timeout=2000)

    def poll(self, timeout):
        self.producer.poll(timeout)

    def __init__(self, host="localhost", port=29092):
        print("Connecting to broker: " + host + ":" + str(port))
        self.conf = {
            'bootstrap.servers': host + ":" + str(port),
            'client.id': socket.gethostname(),
        }
        self.producer = Producer(self.conf)
        admin_client = AdminClient(self.conf)
        topics = admin_client.list_topics().topics

        if not topics:
            raise RuntimeError("Cannot connect to kafka")

    def produce(self, topic, value, key=None):
        if key is None:
            return self.producer.produce(topic, value=value, callback=delivery_callback)
        else:
            return self.producer.produce(topic, key=key, value=value, callback=delivery_callback)
