from macrobase_driver.config import BaseConfig, DriverConfig


class RabbitmqPropertyConfig(BaseConfig):
    host: str = 'localhost'
    port: int = 5672
    user: str = 'rabbitmq'
    password: str = 'test'
    vhost: str = '/'


class QueuePropertyConfig(BaseConfig):
    name: str = 'queue'
    auto_delete: bool = False
    durable: bool = True


class AiopikaDriverConfig(DriverConfig):

    logo: str = """
 _____       _
|  __ \     (_)               
| |  | |_ __ ___   _____ _ __ 
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |   
|_____/|_|  |_| \_/ \___|_|aiopika"""

    rabbitmq: RabbitmqPropertyConfig = RabbitmqPropertyConfig()
    queue: QueuePropertyConfig = QueuePropertyConfig()

    # Processing
    ignore_processed: bool = True
    requeue_delay: int = 10
    default_retry_delay: int = 60
    requeue_unknown: bool = False
    requeue_if_failed: bool = True  # TODO: Set `requeue` for all AiopikaException subclasses
