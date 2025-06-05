from locust import User, task, between, events
import socket
import time
import os

HOST = os.getenv("SOCKET_HOST", "127.0.0.1")
PORT = int(os.getenv("SOCKET_PORT", 65432))

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_and_receive(self, message: bytes) -> bytes:
        self.sock.sendall(message)
        return self.sock.recv(1024)

class SocketUser(User):
    wait_time = between(1, 2)

    def on_start(self):
        self.client = SocketClient(HOST, PORT)
        start_time = time.time()
        try:
            self.client.connect()
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(
                request_type="socket",
                name="connect",
                response_time=total_time,
                response_length=0,
                exception=None
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(
                request_type="socket",
                name="connect",
                response_time=total_time,
                response_length=0,
                exception=e
            )

    def on_stop(self):
        self.client.close()

    @task
    def send_message(self):
        message = b"Hello from Locust!"
        start_time = time.time()
        try:
            data = self.client.send_and_receive(message)
            print(f"Received: {data.decode()}")
            total_time = int((time.time() - start_time) * 1000)
            if data == b"message received":
                self.environment.events.request.fire(
                    request_type="socket",
                    name="send_message",
                    response_time=total_time,
                    response_length=len(data),
                    exception=None
                )
            else:
                self.environment.events.request.fire(
                    request_type="socket",
                    name="send_message",
                    response_time=total_time,
                    response_length=len(data),
                    exception=Exception(f"Unexpected response: {data}")
                )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(
                request_type="socket",
                name="send_message",
                response_time=total_time,
                response_length=0,
                exception=e
            )
