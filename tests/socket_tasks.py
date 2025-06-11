from locust import task
from locust import TaskSet
import time
from test_data.csv_read import CsvRead
import os


class SocketTasks(TaskSet):
    """
    Represents tasks for socket-based performance testing.

    Attributes:
        environment (Environment): The Locust environment instance.

    Methods:
        send_message(): Sends a message to the server and processes the response.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.environment = parent.environment

    @task
    def send_message(self):
        """
        Sends a message to the server, processes the response, and logs metrics.

        The message is read from a CSV file, modified, and encoded before being sent.

        Raises:
            Exception: If the response is unexpected or an error occurs.
        """
        # test_data = CsvRead(os.path.join("tests", "test_data", "sample_messages.csv")).read()
        test_data = CsvRead(os.path.join(os.path.dirname(__file__), 'test_data', 'sample_messages.csv')).read()
        message = (
            test_data["message"].replace("Ø", "0").encode("utf-8")
        )  # Ensure the message is encoded as bytes
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
                    exception=None,
                )
            else:
                self.environment.events.request.fire(
                    request_type="socket",
                    name="send_message",
                    response_time=total_time,
                    response_length=len(data),
                    exception=Exception(f"Unexpected response: {data}"),
                )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(
                request_type="socket",
                name="send_message",
                response_time=total_time,
                response_length=0,
                exception=e,
            )
