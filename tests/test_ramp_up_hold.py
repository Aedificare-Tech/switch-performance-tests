from locust import LoadTestShape


class RampUpHoldShape(LoadTestShape):
    """
    Represents a load test shape for ramping up users, holding them, and ramping down.

    Attributes:
        stages (list): A list of dictionaries defining the duration, users, and spawn rate for each stage.

    Methods:
        tick(): Determines the number of users and spawn rate at the current runtime.
    """

    stages = [
        {"duration": 30, "users": 10, "spawn_rate": 1},  # Ramp up to 10 users in 100s
        {"duration": 60, "users": 10, "spawn_rate": 0.000001},  # Hold 10 users for 60s
        {"duration": 70, "users": 1, "spawn_rate": 1},  # Ramp down to 0 in 40s
  ]

    def tick(self):
        """
        Determines the number of users and spawn rate based on the current runtime.

        Returns:
            tuple: A tuple containing the number of users and spawn rate, or None if the test is complete.
        """
        run_time = self.get_run_time()
        total = 0
        for stage in self.stages:
            total += stage["duration"]
            if run_time < total:
                return (stage["users"], stage["spawn_rate"])
        return None
