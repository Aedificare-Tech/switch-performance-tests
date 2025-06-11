from locust import User, between
from socket_client import SocketClient
from socket_tasks import SocketTasks


class SocketUser(User):
    """
    Represents a Locust user for socket-based performance testing.

    Attributes:
        wait_time (between): The time to wait between tasks.
        tasks (list): The list of tasks to execute.

    Methods:
        on_start(): Initializes the socket client connection.
        on_stop(): Closes the socket client connection.
    """
    wait_time = between(1, 2)
    tasks = [SocketTasks]

    def on_start(self):
        """
        Initializes the socket client connection.

        Raises:
            socket.error: If the connection fails.
        """
        self.client = SocketClient()
        self.client.connect()

    def on_stop(self):
        """
        Closes the socket client connection.

        Raises:
            socket.error: If closing the connection fails.
        """
        self.client.close()
