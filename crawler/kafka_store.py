from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json

class KafkaProd:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce(self, host, url, src):
        self.producer.send('crawled_pages', value={'url': host, 'content': url, 'image_url': src})
        self.producer.flush()

class KafkaCons:
    def __init__(self, group_id):
        self.consumer = KafkaConsumer('crawled_pages', group_id=group_id, auto_offset_reset='earliest')

    def consume(self):
        for msg in self.consumer:
            print(msg)

    