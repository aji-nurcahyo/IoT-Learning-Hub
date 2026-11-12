"""Simulasi GATT profile, fragmentasi ATT MTU, dan estimasi umur baterai BLE."""

from __future__ import annotations

import math


def att_fragments(payload_bytes: int, mtu: int) -> tuple[int, int]:
    """Menghitung jumlah notifikasi ATT dan ukuran payload efektif per PDU."""
    usable_per_pdu = max(1, mtu - 3)
    packets = math.ceil(payload_bytes / usable_per_pdu)
    return packets, usable_per_pdu


def estimate_ble_battery(
    adv_interval_ms: float,
    tx_rx_active_ms: float,
    active_current_ma: float,
    sleep_current_ma: float,
    battery_mah: float,
) -> tuple[float, float]:
    """Menghitung arus rata-rata (mA) dan estimasi umur baterai (hari) untuk mode advertising."""
    sleep_ms = max(0.0, adv_interval_ms - tx_rx_active_ms)
    avg_ma = (
        (tx_rx_active_ms * active_current_ma) + (sleep_ms * sleep_current_ma)
    ) / adv_interval_ms
    hours = battery_mah / avg_ma
    return avg_ma, hours / 24.0


def main() -> None:
    print("=== CHAPTER 17: BLE GATT, ATT MTU & POWER BUDGET SIMULATION ===")

    # 1. Simulasi GATT Attribute Table & Encoding Suhu (0x2A6E, scale 0.01 C, little-endian)
    temp_c = 27.85
    raw_int16 = round(temp_c * 100)
    raw_bytes = raw_int16.to_bytes(2, byteorder="little", signed=True)
    decoded_c = int.from_bytes(raw_bytes, byteorder="little", signed=True) / 100.0
    print(f"[GATT] Service=0x181A Char=0x2A6E temp={temp_c:.2f} C -> bytes={raw_bytes.hex(' ')} -> decoded={decoded_c:.2f} C")

    # 2. Perbandingan Fragmentasi ATT MTU untuk payload JSON/biner 64 byte
    payload_size = 64
    for mtu in (23, 65, 247):
        pkts, eff = att_fragments(payload_size, mtu)
        print(f"[MTU] payload={payload_size} B, ATT_MTU={mtu} -> max_att_payload={eff} B -> packets_needed={pkts}")

    # 3. Estimasi Umur Baterai CR2032 (220 mAh) untuk 3 skenario Advertising Interval
    # Model referensi: event TX+RX 3 kanal ~3.5 ms pada 9.5 mA, deep sleep 0.005 mA (5 uA)
    battery_mah = 220.0
    for adv_ms in (100.0, 500.0, 1000.0, 2000.0):
        avg_ma, days = estimate_ble_battery(
            adv_interval_ms=adv_ms,
            tx_rx_active_ms=3.5,
            active_current_ma=9.5,
            sleep_current_ma=0.005,
            battery_mah=battery_mah,
        )
        print(f"[POWER] adv_interval={adv_ms:6.1f} ms -> I_avg={avg_ma:.4f} mA -> CR2032_life={days:6.1f} days")

    # 4. Perbandingan Notify vs Indicate pada Connection Interval 100 ms
    conn_interval_ms = 100.0
    print(f"[MODE] NOTIFY: throughput max = 1+ PDU per {conn_interval_ms:.0f} ms (tanpa tunggu ATT Confirmation).")
    print(f"[MODE] INDICATE: 1 PDU butuh 1 RTT konfirmasi (~{2 * conn_interval_ms:.0f} ms per transaksi).")


if __name__ == "__main__":
    main()

