import csv
from datetime import datetime
from pathlib import Path

from database import FIELDS, add_product


BASE_DIR = Path(__file__).parent


def log_activity(message):
    logs = BASE_DIR / "logs"
    logs.mkdir(exist_ok=True)
    with (logs / "inventory_log.txt").open("a", encoding="utf-8") as file:
        file.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {message}\n")


def import_csv(con, path):
    inserted, rejected = 0, []
    with Path(path).open(newline="", encoding="utf-8") as file:
        for number, row in enumerate(csv.DictReader(file), 2):
            try:
                add_product(con, row)
                inserted += 1
            except (ValueError, KeyError, Exception) as error:
                rejected.append((number, str(error)))
    log_activity(f"Imported {inserted} products from {path}")
    return inserted, rejected


def export_csv(products):
    reports = BASE_DIR / "reports"
    reports.mkdir(exist_ok=True)
    path = reports / "inventory_report.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(products)
    log_activity("Exported inventory report")
    return path
