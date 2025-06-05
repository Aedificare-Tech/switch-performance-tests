# Socket Server Performance Test Framework

This project provides a performance test framework for a TCP socket server using Locust. It supports advanced user ramp-up, hold, and ramp-down scenarios, and generates detailed HTML/CSV reports for all test metrics.

## Project Structure

- `socket_server.py` — The multi-threaded TCP socket server under test.
- `socket_user.py` — Locust user definition for socket client behavior.
- `test_ramp_up_hold.py` — First test: ramp up to 10 users, hold, then ramp down.
- `test_ramp_up_hold_hold_down.py` — Second test: ramp up to 10 users, hold, ramp down to 5, hold, then finish.
- `runner.py` — Python runner to start/stop tests and generate reports.
- `requirements.txt` — Python dependencies.

## How to Run

1. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Start the socket server:**

   ```sh
   python socket_server.py
   ```

3. **Run the performance test:**

   Use the following command to run the test and generate reports:

   ```sh
   locust -f socket_user.py,test_ramp_up_hold.py --headless --html report.html --csv report --logfile report.log --only-summary
   ```

   This command will:

   - Run the Locust test defined in `socket_user.py` and `test_ramp_up_hold.py`.
   - Generate an HTML report (`report.html`).
   - Save CSV logs (`report_stats.csv`, `report_failures.csv`, etc.).
   - Save detailed logs to `report.log`.

## Reporting

- Locust's built-in reporting captures all performance metrics: response times, failure rates, throughput, percentiles, and more.
- Reports are saved as `report.html`, `report.csv`, and `report.log` by default.

## Customization

- Edit `socket_user.py` to change client behavior.
- Edit test shape files to adjust ramp-up/hold/ramp-down logic.
- Use environment variables `SOCKET_HOST` and `SOCKET_PORT` to target a different server.

---

For questions or improvements, please contact the project maintainer.
