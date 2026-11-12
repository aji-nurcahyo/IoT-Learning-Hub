"""Kalkulator Elektronika Dasar & Power Budget Low-Voltage DC (Chapter 03).

Menghitung:
1. Nilai resistor pembatas arus LED dan disipasi daya (Hukum Ohm & Daya).
2. Arus bocor pull-up resistor saat tombol ditekan.
3. Pembagi tegangan (voltage divider) beserta peringatan batas GPIO 3.3 V.
4. Power budget sederhana untuk node sensor bertenaga baterai LiFePO4 / Li-Ion.
"""

from __future__ import annotations


def led_resistor(v_supply: float, v_forward: float, target_ma: float) -> dict[str, float]:
    """Menghitung R ideal dan mengevaluasi resistor standar terdekat (E12/umum)."""
    i_amp = target_ma / 1000.0
    v_res = v_supply - v_forward
    r_exact = v_res / i_amp
    standard_values = [100, 150, 220, 330, 470, 680, 1000]
    r_chosen = min((r for r in standard_values if r >= r_exact), default=standard_values[-1])
    i_actual_ma = (v_res / r_chosen) * 1000.0
    p_res_mw = (v_res * (i_actual_ma / 1000.0)) * 1000.0
    return {
        "r_exact_ohm": r_exact,
        "r_chosen_ohm": float(r_chosen),
        "i_actual_ma": i_actual_ma,
        "p_res_mw": p_res_mw,
    }


def voltage_divider(v_in: float, r1_ohm: float, r2_ohm: float) -> tuple[float, bool]:
    """Menghitung V_out pembagi tegangan dan cek aman terhadap batas GPIO 3.3 V."""
    v_out = v_in * (r2_ohm / (r1_ohm + r2_ohm))
    safe_3v3 = v_out <= 3.3
    return v_out, safe_3v3


def battery_life_hours(
    capacity_mah: float,
    usable_fraction: float,
    active_ma: float,
    active_s: float,
    sleep_ma: float,
    cycle_s: float,
) -> dict[str, float]:
    """Menghitung arus rata-rata berbasis duty-cycle dan estimasi umur baterai."""
    sleep_s = max(0.0, cycle_s - active_s)
    i_avg_ma = ((active_ma * active_s) + (sleep_ma * sleep_s)) / cycle_s
    effective_mah = capacity_mah * usable_fraction
    hours = effective_mah / i_avg_ma
    return {
        "i_avg_ma": i_avg_ma,
        "effective_mah": effective_mah,
        "hours": hours,
        "days": hours / 24.0,
    }


def main() -> None:
    print("=== KALKULATOR ELEKTRONIKA & POWER BUDGET (CHAPTER 03) ===")

    led = led_resistor(v_supply=3.3, v_forward=2.0, target_ma=6.0)
    print("\n1. LED Current-Limiting Resistor (V_CC=3.3V, V_F=2.0V, Target<=6mA)")
    print(f"   R eksak        : {led['r_exact_ohm']:.1f} ohm")
    print(f"   R standar pilih: {led['r_chosen_ohm']:.0f} ohm")
    print(f"   Arus aktual    : {led['i_actual_ma']:.2f} mA")
    print(f"   Disipasi R     : {led['p_res_mw']:.2f} mW (aman untuk resistor 0.25 W = 250 mW)")

    v_out_safe, is_safe = voltage_divider(v_in=5.0, r1_ohm=10_000, r2_ohm=15_000)
    v_out_bad, is_bad_safe = voltage_divider(v_in=5.0, r1_ohm=4_700, r2_ohm=10_000)
    print("\n2. Level Shifting Sensor 5 V ke GPIO 3.3 V via Voltage Divider")
    print(f"   R1=10k, R2=15k -> V_out = {v_out_safe:.2f} V | Aman <=3.3V: {is_safe}")
    print(f"   R1=4.7k, R2=10k -> V_out = {v_out_bad:.2f} V | Aman <=3.3V: {is_bad_safe} (BAHAYA OVERVOLTAGE!)")

    pb = battery_life_hours(
        capacity_mah=2000.0,
        usable_fraction=0.80,
        active_ma=80.0,
        active_s=3.0,
        sleep_ma=0.15,
        cycle_s=300.0,
    )
    print("\n3. Power Budget Node Sensor (Baterai 2000 mAh, 80% usable, siklus 300 s)")
    print(f"   Arus rata-rata : {pb['i_avg_ma']:.3f} mA")
    print(f"   Kapasitas guna : {pb['effective_mah']:.0f} mAh")
    print(f"   Estimasi umur  : {pb['hours']:.1f} jam (~{pb['days']:.1f} hari)")


if __name__ == "__main__":
    main()

