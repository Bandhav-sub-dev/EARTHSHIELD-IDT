
from pathlib import Path
from datetime import datetime, timezone

LOG_FILE = Path(__file__).resolve().parents[2] / "logs" / "earthshield.log"


def log(level, message):
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"[{timestamp}] [{level.upper()}] {message}"

    print(line)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(line + "\n")


def info(message):
    log("INFO", message)


def warning(message):
    log("WARNING", message)


def error(message):
    log("ERROR", message)


def success(message):
    log("PASS", message)
