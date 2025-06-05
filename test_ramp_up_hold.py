from locust import LoadTestShape

class RampUpHoldDownShape(LoadTestShape):
    """
    First Test: Start with 1 user, ramp up by 1 every 10s to 10, hold for 60s, then ramp down.
    """
    stages = [
        {"duration": 30, "users": 10, "spawn_rate": 1},  # 10 users in 90s (1 every 10s)
        {"duration": 60, "users": 10, "spawn_rate": 0.0001},   # Hold 10 users for 60s
        {"duration": 70, "users": 1, "spawn_rate": 1},   # Ramp down to 1 in 10s
    ]

    def tick(self):
        run_time = self.get_run_time()
        total = 0
        for stage in self.stages:
            total += stage["duration"]
            if run_time < total:
                return (stage["users"], stage["spawn_rate"])
        return None
