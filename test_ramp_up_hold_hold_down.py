from locust import LoadTestShape

class RampUpHoldHoldDownShape(LoadTestShape):
    """
    Second Test: Start with 1 user, ramp up by 1 every 10s to 10, hold for 30s, ramp down to 5, hold 5 for 30s, then finish.
    """
    stages = [
        {"duration": 90, "users": 10, "spawn_rate": 0.1},  # 10 users in 90s (1 every 10s)
        {"duration": 120, "users": 10, "spawn_rate": 0},   # Hold 10 users for 30s
        {"duration": 130, "users": 5, "spawn_rate": 0.5},  # Ramp down to 5 in 10s
        {"duration": 160, "users": 5, "spawn_rate": 0},    # Hold 5 users for 30s
        {"duration": 170, "users": 0, "spawn_rate": 5},    # Ramp down to 0 in 10s
    ]

    def tick(self):
        run_time = self.get_run_time()
        total = 0
        for stage in self.stages:
            total += stage["duration"]
            if run_time < total:
                return (stage["users"], stage["spawn_rate"])
        return None
