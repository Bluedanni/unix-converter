#!/usr/bin/env python3

from datetime import datetime
from zoneinfo import ZoneInfo
import argparse


def print_banner():
    print("""
                            === Unix Time Converter ===
""")

# =========================
# Timezones
# =========================
TIMEZONES = {
    "1": ("UTC", "UTC"),
    "2": ("Sydney (AEST/AEDT)", "Australia/Sydney"),
    "3": ("Perth (AWST)", "Australia/Perth"),
    "4": ("London (UK)", "Europe/London"),
    "5": ("Rome (Italy)", "Europe/Rome"),
    "6": ("Berlin (EU Central)", "Europe/Berlin"),
    "7": ("New York (US Eastern)", "America/New_York"),
    "8": ("Singapore (APAC)", "Asia/Singapore"),
}

# =========================
# Parse arguments
# =========================
def get_args():
    parser = argparse.ArgumentParser(
        description="Unix timestamp converter with timezone support"
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Input file containing Unix timestamps"
    )
    parser.add_argument(
        "--sort",
        action="store_true",
        help="Sort timestamps chronologically (optional)"
    )
    return parser.parse_args()

# =========================
# Parse epoch safely
# =========================
def parse_epoch(raw):
    value = float(raw)

    if value > 1e14:
        return value / 1_000_000, "microseconds"
    elif value > 1e11:
        return value / 1_000, "milliseconds"
    else:
        return value, "seconds"

# =========================
# Convert timestamp
# =========================
def convert(raw, tz_name):
    seconds, fmt = parse_epoch(raw)

    utc_dt = datetime.fromtimestamp(seconds, tz=ZoneInfo("UTC"))
    local_dt = utc_dt.astimezone(ZoneInfo(tz_name))

    return fmt, local_dt, seconds  # include numeric for optional sorting

# =========================
# Select timezone
# =========================
def select_timezone():
    print("\nSelect timezone:\n")

    for key, (label, _) in TIMEZONES.items():
        print(f"{key}. {label}")

    choice = input("\nEnter choice: ").strip()

    return TIMEZONES.get(choice, None)

# =========================
# Load and process file
# =========================
def load_data(file_path, tz_label, tz_name, do_sort):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    entries = []

    for line in lines:
        raw = line

        try:
            fmt, dt, seconds = convert(raw, tz_name)

            entries.append((
                seconds,   # used only if sorting enabled
                raw,
                fmt,
                tz_label,
                dt
            ))

        except Exception:
            entries.append((
                float("inf"),
                raw,
                "ERROR",
                tz_label,
                "INVALID"
            ))

    if do_sort:
        entries.sort(key=lambda x: x[0])

    return entries

# =========================
# CLI output (aligned table)
# =========================
def print_table(entries):
    print("\n================ RESULTS ================\n")

    print(f"{'RAW':<25} | {'FORMAT':<12} | {'TIMEZONE':<20} | CONVERTED")
    print("-" * 100)

    for _, raw, fmt, tz, dt in entries:

        if dt == "INVALID":
            converted = "ERROR"
        else:
            converted = dt.isoformat(timespec="milliseconds")

        print(
            f"{raw:<25} | "
            f"{fmt:<12} | "
            f"{tz:<20} | "
            f"{converted}"
        )

# =========================
# MAIN
# =========================
def main():
    print_banner()
    args = get_args()

    tz_choice = select_timezone()

    if not tz_choice:
        print("Invalid selection.")
        return

    tz_label, tz_name = tz_choice

    entries = load_data(args.file, tz_label, tz_name, args.sort)

    print_table(entries)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
