import os
from pydantic_settings import BaseSettings


# class RabbitMqConsumerSettings:
#     """Common settings for this project"""

#     rmq_host: str = os.environ.get("rabbitmq_host")
#     rmq_username: str = os.environ.get("rmq_username")
#     rmq_password: str = os.environ.get("rmq_password")
#     rmq_vhost: str = os.environ.get("rmq_vhost")
#     queue_name: str = os.environ.get("queue_name")
#     rmq_port: int = int(os.environ.get("rmq_port", 5672))


class Settings(BaseSettings):
    """Common settings for this project"""

    openai_api_key: str