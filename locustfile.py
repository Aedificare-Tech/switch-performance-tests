"""
Locust test framework for the socket server.

Usage:
    locust -f locustfile.py --headless -u 10 -r 2 --run-time 1m

You can override host/port with environment variables or by editing below.
"""
import os
from locust import User, task, between, events
import socket
import time

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
        try:
            self.client.connect()
        except Exception as e:
            events.request_failure.fire(
                request_type="socket",
                name="connect",
                response_time=0,
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
            total_time = int((time.time() - start_time) * 1000)
            if data == b"message received":
                events.request_success.fire(
                    request_type="socket",
                    name="send_message",
                    response_time=total_time,
                    response_length=len(data)
                )
            else:
                events.request_failure.fire(
                    request_type="socket",
                    name="send_message",
                    response_time=total_time,
                    exception=Exception(f"Unexpected response: {data}")
                )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="socket",
                name="send_message",
                response_time=total_time,
                exception=e
            )
