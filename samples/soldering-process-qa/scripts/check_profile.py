"""Minimal helper: print peak temperature from a CSV column named peak_c."""
import csv
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "profile.csv"
with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
peaks = [float(r["peak_c"]) for r in rows if r.get("peak_c")]
print(f"samples={len(peaks)} max_peak_c={max(peaks) if peaks else 'n/a'}")
