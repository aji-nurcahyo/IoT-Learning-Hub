"""Kalibrasi Dua Titik & Propagasi Ketidakpastian Pengukuran pada Data Referensi Sintetis (Chapter 08).

Menggunakan dataset telemetry.csv (source=synthetic) yang berisi:
- 5 titik kurva perbandingan terhadap suhu referensi (0.0 C .. 60.0 C)
- 5 pengulangan pengukuran pada titik 25.0 C untuk estimasi random error (Type A)

Menghitung:
1. Koefisien kalibrasi dua titik (0 C dan 60 C) -> slope m dan offset b.
2. Perbandingan RMSE sebelum vs sesudah kalibrasi.
3. Ketidakpastian gabungan u_c = sqrt(u_A^2 + u_B_ref^2 + u_B_res^2) dan expanded U (k=2).
"""

from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path


def main() -> None:
    csv_path = Path(__file__).resolve().parent.parent / "telemetry.csv"
    cal_points: list[tuple[float, float]] = []
    repeat_raw: list[float] = []

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            ref = float(row["ref_temp_c"])
            raw = float(row["raw_sensor_c"])
            if row["trial_group"] == "cal_curve":
                cal_points.append((ref, raw))
            elif row["trial_group"] == "repeat_25c":
                repeat_raw.append(raw)

    # 1. Kalibrasi dua titik menggunakan titik terendah (0 C) dan tertinggi (60 C)
    ref_low, raw_low = cal_points[0]
    ref_high, raw_high = cal_points[-1]
    slope = (ref_high - ref_low) / (raw_high - raw_low)
    offset = ref_low - slope * raw_low

    # 2. RMSE sebelum dan sesudah kalibrasi di seluruh 5 titik kurva
    sq_err_before = [(raw - ref) ** 2 for ref, raw in cal_points]
    sq_err_after = [((slope * raw + offset) - ref) ** 2 for ref, raw in cal_points]
    rmse_before = math.sqrt(sum(sq_err_before) / len(cal_points))
    rmse_after = math.sqrt(sum(sq_err_after) / len(cal_points))

    # 3. Analisis ketidakpastian pada pengulangan 25.0 C
    cal_repeats = [slope * x + offset for x in repeat_raw]
    mean_cal = statistics.mean(cal_repeats)
    std_dev = statistics.stdev(cal_repeats)
    u_type_a = std_dev / math.sqrt(len(cal_repeats))

    # Type B: termometer referensi akurasi +-0.10 C (rectangular -> / sqrt(3))
    #         resolusi ADC setara 0.05 C (rectangular -> / sqrt(12) untuk +/-0.025)
    u_b_ref = 0.10 / math.sqrt(3.0)
    u_b_res = 0.05 / math.sqrt(12.0)

    u_combined = math.sqrt(u_type_a**2 + u_b_ref**2 + u_b_res**2)
    u_expanded = 2.0 * u_combined  # ~95% tingkat kepercayaan (k=2)

    print("=== ANALISIS KALIBRASI & KETIDAKPASTIAN PENGUKURAN (CHAPTER 08) ===")
    print(f"Dataset sintetis: {csv_path.name} (source=synthetic)")
    print(f"Titik kalibrasi : Low=({raw_low:.2f} -> {ref_low:.2f} C), High=({raw_high:.2f} -> {ref_high:.2f} C)")
    print(f"Model kalibrasi : T_cal = {slope:.4f} * T_raw + ({offset:.4f})")
    print(f"RMSE sebelum kalibrasi : {rmse_before:.4f} C")
    print(f"RMSE sesudah kalibrasi : {rmse_after:.4f} C")
    print("\n--- Evaluasi Ketidakpastian pada Titik Referensi 25.00 C (n=5) ---")
    print(f"Rata-rata terkalibrasi : {mean_cal:.3f} C (Std Dev s = {std_dev:.4f} C)")
    print(f"u_A (random mean)      : {u_type_a:.4f} C")
    print(f"u_B (ref +-0.10 C)     : {u_b_ref:.4f} C")
    print(f"u_B (resolusi 0.05 C)  : {u_b_res:.4f} C")
    print(f"u_c (gabungan)         : {u_combined:.4f} C")
    print(f"Hasil lapor (k=2, 95%) : {mean_cal:.2f} +/- {u_expanded:.2f} C")


if __name__ == "__main__":
    main()

