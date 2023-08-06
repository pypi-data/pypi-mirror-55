from macrobase_driver.config import DriverConfig

from sanic.config import Config


class SanicDriverConfig(DriverConfig):

    logo: str = """
 _____       _
|  __ \     (_)               
| |  | |_ __ ___   _____ _ __ 
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |   
|_____/|_|  |_| \_/ \___|_|sanic
    """

    workers: int = 1
    health_endpoint: bool = True

    host: str = '0.0.0.0'
    port: int = 8000
    blueprint: str = ''

    request_max_size = 100000000  # 100 megabytes
    request_timeout = 60  # 60 seconds
    response_timeout = 60  # 60 seconds
    keep_alive = True
    keep_alive_timeout = 5  # 5 seconds
    websocket_max_size = 2 ** 20  # 1 megabytes
    websocket_max_queue = 32
    websocket_read_limit = 2 ** 16
    websocket_write_limit = 2 ** 16
    graceful_shutdown_timeout = 15.0  # 15 sec
    access_log = True

    def get_sanic_config(self) -> Config:
        c = Config()
        c.LOGO = self.logo
        c.REQUEST_MAX_SIZE = self.request_max_size
        c.REQUEST_TIMEOUT = self.request_timeout
        c.RESPONSE_TIMEOUT = self.response_timeout
        c.KEEP_ALIVE = self.keep_alive
        c.KEEP_ALIVE_TIMEOUT = self.keep_alive_timeout
        c.WEBSOCKET_MAX_SIZE = self.websocket_max_size
        c.WEBSOCKET_MAX_QUEUE = self.websocket_max_queue
        c.WEBSOCKET_READ_LIMIT = self.websocket_read_limit
        c.WEBSOCKET_WRITE_LIMIT = self.websocket_write_limit
        c.GRACEFUL_SHUTDOWN_TIMEOUT = self.graceful_shutdown_timeout
        c.ACCESS_LOG = self.access_log

        return c
