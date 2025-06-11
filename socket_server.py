import socket
import threading
import time
import random

HOST = "0.0.0.0"  # Configured to Localhost for testing
PORT = 9000  # Port to listen on
# Server listening on 127.0.0.1:65432


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Connection closed by {addr}")
                break
            # print(f"Received from {addr}: {data.decode()}")
            sleep_duration = random.randint(2, 5)
            time.sleep(sleep_duration)  # Adding a delay to simulate processing time
            conn.sendall(b"message received")  # Removed unnecessary decode


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
