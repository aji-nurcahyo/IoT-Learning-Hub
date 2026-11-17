"""
Chapter 31: Low-Power Design, Sleep Modes & Energy Measurement
Model kalkulasi profil konsumsi daya baterai, duty cycle sensor, dan estimasi masa pakai.
"""

from typing import Dict, List, Any


def calculate_average_current(
    active_current_ma: float,
    active_time_s: float,
    sleep_current_ua: float,
    sleep_time_s: float,
) -> float:
    """Menghitung arus rata-rata (mA) pada satu siklus duty cycling."""
    total_time_s = active_time_s + sleep_time_s
    sleep_current_ma = sleep_current_ua / 1000.0
    charge_mas = (active_current_ma * active_time_s) + (sleep_current_ma * sleep_time_s)
    return charge_mas / total_time_s


def estimate_battery_lifetime(
    capacity_mah: float,
    average_current_ma: float,
    derating_factor: float = 0.85,
    self_discharge_percent_per_year: float = 2.0,
) -> Dict[str, float]:
    """Mengestimasi masa pakai baterai (jam, hari, tahun) dengan faktor derating."""
    usable_capacity_mah = capacity_mah * derating_factor
    hours = usable_capacity_mah / average_current_ma
    days = hours / 24.0
    years_raw = days / 365.25
    # Menghitung penyesuaian self-discharge tahunan
    # Q(t) = Q0 * (1 - self_discharge * t)
    years_adjusted = years_raw * (1.0 - (self_discharge_percent_per_year / 100.0) * (years_raw / 10.0))
    years_final = max(0.01, min(years_raw, years_adjusted))

    return {
        "usable_capacity_mah": usable_capacity_mah,
        "average_current_ma": average_current_ma,
        "lifetime_hours": round(hours, 2),
        "lifetime_days": round(days, 2),
        "lifetime_years": round(years_final, 2),
    }


def run_power_simulation() -> None:
    print("=== CHAPTER 31: LOW-POWER & BATTERY LIFETIME VERIFICATION ===")
    
    # Skenario 1: Profil Agresif (Pengambilan sampel tiap 60 detik)
    avg_i1 = calculate_average_current(
        active_current_ma=120.0,
        active_time_s=1.5,
        sleep_current_ua=10.0,
        sleep_time_s=58.5,
    )
    res1 = estimate_battery_lifetime(capacity_mah=2500.0, average_current_ma=avg_i1)
    print(f"[SCENARIO 1 - Interval 60s] I_avg: {avg_i1:.4f} mA | Lifetime: {res1['lifetime_days']:.1f} hari ({res1['lifetime_years']:.2f} tahun)")

    # Skenario 2: Profil Konservatif (Deep sleep 10 menit = 600 detik)
    avg_i2 = calculate_average_current(
        active_current_ma=120.0,
        active_time_s=1.5,
        sleep_current_ua=10.0,
        sleep_time_s=598.5,
    )
    res2 = estimate_battery_lifetime(capacity_mah=2500.0, average_current_ma=avg_i2)
    print(f"[SCENARIO 2 - Interval 600s] I_avg: {avg_i2:.4f} mA | Lifetime: {res2['lifetime_days']:.1f} hari ({res2['lifetime_years']:.2f} tahun)")

    # Skenario 3: ULP / Sensor Power Gating (Aktif 500ms, Deep sleep 30 menit = 1800 detik)
    avg_i3 = calculate_average_current(
        active_current_ma=80.0,
        active_time_s=0.5,
        sleep_current_ua=5.0,
        sleep_time_s=1799.5,
    )
    res3 = estimate_battery_lifetime(capacity_mah=2500.0, average_current_ma=avg_i3)
    print(f"[SCENARIO 3 - Sensor Gating 1800s] I_avg: {avg_i3:.4f} mA | Lifetime: {res3['lifetime_days']:.1f} hari ({res3['lifetime_years']:.2f} tahun)")

    assert avg_i1 > avg_i2 > avg_i3, "Logika penurunan arus rata-rata gagal!"
    assert res3["lifetime_years"] > res2["lifetime_years"] > res1["lifetime_years"], "Relasi masa pakai baterai salah!"
    print("STATUS: VERIFIED (Semua pengujian model konsumsi energi lulus 100%)")


if __name__ == "__main__":
    run_power_simulation()
