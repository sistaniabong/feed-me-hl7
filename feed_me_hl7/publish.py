import pika
import click
from settings import RabbitMqConsumerSettings


@click.command()
@click.option(
    "--message", required=True
)
def publish(message: str):
    """
    Publish a message to the RabbitMQ queue.
    """
    print(f"Publishing message: {message}")
    settings = RabbitMqConsumerSettings()
    credentials = pika.PlainCredentials(
            settings.rmq_username, settings.rmq_password
        )
   
    ssl_options = None

    connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.rmq_host,
                port=settings.rmq_port,
                credentials=credentials,
                virtual_host=settings.rmq_vhost,
                ssl_options=ssl_options,
            )
        )

    channel = connection.channel()

    # Make sure the queue exists
    channel.queue_declare(queue=settings.queue_name, durable=True)

    # Publish the message
    channel.basic_publish(
        exchange='',
        routing_key='hl7',
        body=message)

    print(f" [x] Sent {message}")
    connection.close()


if __name__ == "__main__":
    publish()
