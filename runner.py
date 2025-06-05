import subprocess
import os

class LocustRunner:
    def __init__(self, test_file, user_file, report_file="report.html"):
        self.test_file = test_file
        self.user_file = user_file
        self.report_file = report_file
        self.process = None

    def start(self):
        cmd = [
            "locust",
            "-f", self.user_file, self.test_file,
            "--headless",
            "--html", self.report_file,
            "--csv", self.report_file.replace('.html', ''),
            "--logfile", self.report_file.replace('.html', '.log'),
            "--only-summary"
        ]
        self.process = subprocess.Popen(cmd)
        print(f"Started Locust with command: {' '.join(cmd)}")

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("Locust test stopped.")
