"""Acceptance Test Harness untuk Logika Firmware Capstone (Chapter 10).

Mereplikasi persamaan konversi NTC Beta + kalibrasi 2-titik, kontrol histeresis
(AUTO_NORMAL 28..30 C, AUTO_STRICT 25..27 C, MANUAL_ON), serta mekanisme
FAIL_SAFE (INTERLOCK_OPEN & SENSOR_FAULT_NAN) dari capstone_env_monitor.ino,
lalu memverifikasi seluruh 12 skenario uji pada telemetry.csv (synthetic).
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

V_SUPPLY_MV = 3300.0
R_FIXED_OHM = 10000.0
NTC_R25_OHM = 10000.0
NTC_BETA_K = 3950.0
T25_KELVIN = 298.15
CAL_SLOPE = 1.0381
CAL_OFFSET = -1.4740


def convert_mv_to_calibrated_c(mv: float) -> float | None:
    if mv < 100.0 or mv > 3200.0:
        return None
    r_ntc = R_FIXED_OHM * (mv / (V_SUPPLY_MV - mv))
    inv_t = (1.0 / T25_KELVIN) + (1.0 / NTC_BETA_K) * math.log(r_ntc / NTC_R25_OHM)
    raw_c = (1.0 / inv_t) - 273.15
    return CAL_SLOPE * raw_c + CAL_OFFSET


def main() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "telemetry.csv"
    mode = "AUTO_NORMAL"
    mode_before_fault = "AUTO_NORMAL"
    fan_on = False
    passed = 0
    total = 0

    print("=== ACCEPTANCE TEST HARNESS CAPSTONE LEVEL 1 (CHAPTER 10) ===")
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            total += 1
            step = int(row["step"])
            t_ms = int(row["t_ms"])
            mv = float(row["raw_mv"])
            btn_press = row["btn_press"].lower() == "true"
            interlock_open = row["interlock_open"].lower() == "true"
            exp_mode = row["expected_mode"]
            exp_fan = row["expected_fan"]

            if btn_press and mode != "FAULT_SAFE":
                mode = {"AUTO_NORMAL": "AUTO_STRICT", "AUTO_STRICT": "MANUAL_ON", "MANUAL_ON": "AUTO_NORMAL"}[mode]
                mode_before_fault = mode

            temp_c = convert_mv_to_calibrated_c(mv)

            if interlock_open:
                mode = "FAULT_SAFE"
                fan_on = False
                alarm = True
                fault = "INTERLOCK_OPEN"
            elif temp_c is None:
                mode = "FAULT_SAFE"
                fan_on = False
                alarm = True
                fault = "SENSOR_FAULT_NAN"
            else:
                if mode == "FAULT_SAFE":
                    mode = mode_before_fault
                fault = "NONE"
                alarm = temp_c >= 45.0
                if mode == "MANUAL_ON":
                    fan_on = True
                else:
                    t_high, t_low = (27.0, 25.0) if mode == "AUTO_STRICT" else (30.0, 28.0)
                    if not fan_on and temp_c >= t_high:
                        fan_on = True
                    elif fan_on and temp_c <= t_low:
                        fan_on = False

            fan_str = "ON" if fan_on else "OFF"
            assert mode == exp_mode and fan_str == exp_fan, (
                f"Step {step} gagal: got ({mode}, {fan_str}), expected ({exp_mode}, {exp_fan})"
            )
            passed += 1
            pkt = {
                "seq": step,
                "uptime_ms": t_ms,
                "temp_c": round(temp_c, 2) if temp_c is not None else None,
                "mode": mode,
                "fan": fan_str,
                "alarm": alarm,
                "fault": fault,
            }
            print(f"[PASS #{step:02d}] {json.dumps(pkt)}")

    print("-" * 72)
    print(f"Hasil Acceptance Test (Software Logic): {passed}/{total} skenario LULUS")


if __name__ == "__main__":
    main()

