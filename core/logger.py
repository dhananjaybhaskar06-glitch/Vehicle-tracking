import csv
import os
from datetime import datetime

LOG_FILE = "logs/events.csv"

os.makedirs("logs", exist_ok=True)

def log_event(event, severity):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Time","Event","Severity"])

        writer.writerow([datetime.now(), event, severity])