"""Simulasi Kuantisasi ADC 12-bit, Reduksi Noise Moving Average & Aliasing Nyquist (Chapter 07).

Menunjukkan secara kuantitatif:
1) Resolusi kuantisasi ADC 12-bit (LSB pada referensi 3.3 V) dan ketidakpastian kuantisasi.
2) Reduksi simpangan baku (noise) oleh Moving Average 8-sampel pada telemetry.csv (sintetis).
3) Fenomena aliasing ketika sinyal 60 Hz disampling pada 80 Hz (< 2 * 60 Hz).
"""

from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path


def main() -> None:
    print("=== SIMULASI ADC, FILTERING & NYQUIST ALIASING (CHAPTER 07) ===")

    # 1. Kuantisasi 12-bit
    v_fs = 3.30
    bits = 12
    levels = (1 << bits) - 1
    lsb_mv = (v_fs / levels) * 1000.0
    print(f"1. ADC 12-bit (V_FS={v_fs:.2f} V): {levels + 1} level, 1 LSB = {lsb_mv:.4f} mV")
    print(f"   Ketidakpastian kuantisasi ideal = +/-{lsb_mv / 2.0:.4f} mV")

    # 2. Moving Average pada data sintetis telemetry.csv
    csv_path = Path(__file__).resolve().parent.parent / "telemetry.csv"
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        raw_codes = [int(r["adc_raw_noisy"]) for r in csv.DictReader(handle)]

    raw_mv = [(c / levels) * v_fs * 1000.0 for c in raw_codes]
    window = 4
    ma_mv = [sum(raw_mv[i - window + 1 : i + 1]) / window for i in range(window - 1, len(raw_mv))]

    print("\n2. Uji Moving Average (N=4) pada telemetry.csv (true_mv=1650.0 mV):")
    print(f"   Std dev mentah          : {statistics.stdev(raw_mv):.2f} mV")
    print(f"   Std dev setelah filter  : {statistics.stdev(ma_mv):.2f} mV")
    print(f"   Rata-rata akhir terfilter: {ma_mv[-1]:.2f} mV")

    # 3. Bukti Aliasing Nyquist: sinyal 60 Hz disampling pada f_s = 80 Hz
    f_sig = 60.0
    f_s = 80.0
    f_alias = abs(f_sig - f_s)
    # Cek apakah nilai sampel pada t_n = n / f_s identik (terbalik fasa) dengan sin(2*pi*20*t)
    max_diff = 0.0
    for n in range(16):
        t = n / f_s
        x_true = math.sin(2.0 * math.pi * f_sig * t)
        x_alias = -math.sin(2.0 * math.pi * f_alias * t)
        max_diff = max(max_diff, abs(x_true - x_alias))
    print(f"\n3. Uji Nyquist: f_sig={f_sig:.0f} Hz, f_s={f_s:.0f} Hz (< 2*f_sig = 120 Hz)")
    print(f"   Frekuensi alias terhitung : {f_alias:.1f} Hz")
    print(f"   Deviasi sampel 60Hz vs -sin(20Hz): {max_diff:.2e} (identik secara diskrit!)")


if __name__ == "__main__":
    main()

