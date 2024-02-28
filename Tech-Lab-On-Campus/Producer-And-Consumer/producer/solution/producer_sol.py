from producer_interface import mqProducerInterface
import pika
import os

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name:str) -> None:
        self.key = routing_key
        self.name = exchange_name
        self.setupRMQConnection()
    
    def setupRMQConnection(self) -> None:
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()
        self.exchange = self.channel.exchange_declare(exchange=self.name)

    def publishOrder(self, message: str) -> None:
        self.channel.basic_publish(
            exchange=self.name,
            routing_key=self.key,
            body=message,
        )
        self.channel.close()
        self.connection.close() 