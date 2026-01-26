from datetime import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "api.log")
LOG_FILE = os.path.abspath(LOG_FILE)

def log_event(event: str, detail: str = ""):
    timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
    line = f"[{timestamp}] {event} {detail}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
