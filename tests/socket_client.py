import socket
import os

# HOST = os.getenv("SOCKET_HOST", "127.0.0.1")
# PORT = int(os.getenv("SOCKET_PORT", 65432))

HOST = "host.docker.internal"  # Default to 'internal for local testing' for Docker networking
PORT = 9000


class SocketClient:
    """
    Manages TCP socket connections for sending and receiving messages.

    Attributes:
        host (str): The server host address.
        port (int): The server port number.
        sock (socket.socket): The socket instance.

    Methods:
        connect(): Establishes a connection to the server.
        close(): Closes the connection to the server.
        send_and_receive(message): Sends a message to the server and receives the response.
    """

    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        """
        Establishes a connection to the server.

        Raises:
            socket.error: If the connection fails.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        """
        Closes the connection to the server.

        Raises:
            socket.error: If closing the connection fails.
        """
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_and_receive(self, message: bytes) -> bytes:
        """
        Sends a message to the server and receives the response.

        Args:
            message (bytes): The message to send.

        Returns:
            bytes: The response from the server.

        Raises:
            socket.error: If sending or receiving fails.
        """
        self.sock.sendall(message)
        return self.sock.recv(1024)
