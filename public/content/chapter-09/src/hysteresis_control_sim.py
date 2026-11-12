"""Simulasi Kontrol Threshold Tunggal vs Histeresis + Fail-Safe Sensor Fault (Chapter 09).

Menggunakan trace suhu ber-noise pada telemetry.csv (source=synthetic) untuk membandingkan:
1) Single-threshold bang-bang control (T >= 30.0 C) -> mengalami chattering ON/OFF berulang!
2) Hysteresis control (ON >= 30.0 C, OFF <= 28.0 C) + Fail-Safe saat sensor NaN -> stabil & aman!
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

T_HIGH = 30.0
T_LOW = 28.0


def main() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "telemetry.csv"
    rows: list[tuple[int, float, bool]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        for r in csv.DictReader(handle):
            val = float(r["temp_c"]) if r["temp_c"].lower() != "nan" else math.nan
            rows.append((int(r["step"]), val, r["fault_flag"].lower() == "true"))

    # 1. Single-threshold tanpa histeresis (mengabaikan deadband)
    single_state = False
    single_transitions = 0
    for _, temp, fault in rows:
        if fault or math.isnan(temp):
            new_state = False
        else:
            new_state = temp >= T_HIGH
        if new_state != single_state:
            single_transitions += 1
            single_state = new_state

    # 2. Kontrol Histeresis + Fail-Safe
    hyst_state = False
    hyst_transitions = 0
    print("=== SIMULASI KONTROL HISTERESIS & FAIL-SAFE (CHAPTER 09) ===")
    for step, temp, fault in rows:
        if fault or math.isnan(temp):
            if hyst_state:
                hyst_transitions += 1
            hyst_state = False
            print(f"step={step:2d} | temp=  NaN | STATUS=FAIL_SAFE_OFF (Alarm ON)")
            continue

        prev = hyst_state
        if not hyst_state and temp >= T_HIGH:
            hyst_state = True
        elif hyst_state and temp <= T_LOW:
            hyst_state = False
        if hyst_state != prev:
            hyst_transitions += 1

        print(f"step={step:2d} | temp={temp:5.2f} C | fan={'ON ' if hyst_state else 'OFF'}")

    print("-" * 60)
    print(f"Jumlah transisi (Single-Threshold 30.0 C) : {single_transitions} kali (CHATTERING!)")
    print(f"Jumlah transisi (Histeresis 28.0..30.0 C) : {hyst_transitions} kali (STABIL)")


if __name__ == "__main__":
    main()

