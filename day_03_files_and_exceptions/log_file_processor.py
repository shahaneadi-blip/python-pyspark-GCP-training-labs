from collections import Counter
from datetime import datetime
from pathlib import Path


class InvalidLogEntryError(Exception):
    pass


LEVELS = {"INFO", "WARNING", "ERROR", "DEBUG"}
BASE_DIR = Path(__file__).parent


def parse_entry(line):
    parts = line.strip().split(maxsplit=3)
    if len(parts) != 4:
        raise InvalidLogEntryError("Expected date, time, level, and message")
    date_text, time_text, level, message = parts
    try:
        timestamp = datetime.strptime(f"{date_text} {time_text}", "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise InvalidLogEntryError("Invalid date or time") from error
    if level not in LEVELS:
        raise InvalidLogEntryError("Unknown log level")
    if not message.strip():
        raise InvalidLogEntryError("Missing message")
    return {"timestamp": timestamp, "level": level, "message": message}


def analyse(path):
    entries = []
    invalid = []
    with path.open(encoding="utf-8") as file:
        for number, line in enumerate(file, 1):
            if not line.strip():
                invalid.append((number, line.rstrip(), "Empty record"))
                continue
            try:
                entries.append(parse_entry(line))
            except InvalidLogEntryError as error:
                invalid.append((number, line.rstrip(), str(error)))
    return entries, invalid


def write_reports(path, entries, invalid):
    counts = Counter(entry["level"] for entry in entries)
    errors = [entry for entry in entries if entry["level"] == "ERROR"]
    warnings = [entry for entry in entries if entry["level"] == "WARNING"]
    error_path = BASE_DIR / "error_report.txt"
    summary_path = BASE_DIR / "log_report.txt"
    error_path.write_text("\n".join(f"{entry['timestamp']:%Y-%m-%d %H:%M:%S} {entry['message']}" for entry in errors) + "\n", encoding="utf-8")
    lines = [
        "LOG FILE ANALYSIS REPORT",
        f"File: {path.name}",
        f"Total records: {len(entries) + len(invalid)}",
        f"Valid records: {len(entries)}",
        f"Invalid records: {len(invalid)}",
        f"INFO: {counts['INFO']}",
        f"WARNING: {counts['WARNING']}",
        f"ERROR: {counts['ERROR']}",
        f"DEBUG: {counts['DEBUG']}",
        "Errors:",
    ]
    lines.extend(f"{entry['timestamp']:%Y-%m-%d %H:%M:%S} {entry['message']}" for entry in errors)
    lines.append("Warnings:")
    lines.extend(f"{entry['timestamp']:%Y-%m-%d %H:%M:%S} {entry['message']}" for entry in warnings)
    lines.append("Invalid records:")
    lines.extend(f"Line {number}: {reason} | {record}" for number, record, reason in invalid)
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return error_path, summary_path


def main():
    requested = input("Log file path [application.log]: ").strip()
    path = Path(requested) if requested else BASE_DIR / "application.log"
    try:
        entries, invalid = analyse(path)
    except FileNotFoundError:
        print("Log file not found.")
        return
    except PermissionError:
        print("Permission denied while reading the log file.")
        return
    error_path, summary_path = write_reports(path, entries, invalid)
    print(f"Processed {len(entries)} valid and {len(invalid)} invalid records.")
    print(f"Reports: {error_path.name}, {summary_path.name}")


if __name__ == "__main__":
    main()
