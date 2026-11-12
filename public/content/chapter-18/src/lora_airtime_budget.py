"""Kalkulator Time-on-Air (ToA) LoRa PHY (Semtech AN1200.13) & Link Budget."""

from __future__ import annotations

import math


# Sensitivitas tipikal chip transceiver LoRa (BW=125 kHz, referensi datasheet Semtech SX1276)
TYPICAL_SENSITIVITY_DBM_BW125 = {
    7: -123.0,
    8: -126.0,
    9: -129.0,
    10: -132.0,
    11: -134.5,
    12: -137.0,
}


def lora_time_on_air_ms(
    sf: int,
    bw_hz: int = 125_000,
    payload_bytes: int = 24,
    cr_den: int = 5,
    preamble_symbols: int = 8,
    explicit_header: bool = True,
    crc_enabled: bool = True,
) -> tuple[float, float, int]:
    """Menghitung durasi simbol (ms), total Time-on-Air (ms), dan status DE (Low Data Rate Opt)."""
    t_sym_ms = (2**sf / bw_hz) * 1000.0
    de = 1 if t_sym_ms >= 16.0 else 0
    ih = 0 if explicit_header else 1
    crc = 1 if crc_enabled else 0
    cr_param = cr_den - 4  # 1=4/5 .. 4=4/8

    t_preamble_ms = (preamble_symbols + 4.25) * t_sym_ms
    num = 8 * payload_bytes - 4 * sf + 28 + 16 * crc - 20 * ih
    den = 4 * (sf - 2 * de)
    n_payload = 8 + max(math.ceil(num / den) * (cr_param + 4), 0)
    t_payload_ms = n_payload * t_sym_ms
    return t_sym_ms, t_preamble_ms + t_payload_ms, de


def fspl_db(distance_km: float, freq_mhz: float) -> float:
    """Free-Space Path Loss teoritis (dB)."""
    return 32.44 + 20.0 * math.log10(distance_km) + 20.0 * math.log10(freq_mhz)


def main() -> None:
    print("=== CHAPTER 18: LORA PHY TIME-ON-AIR & LINK BUDGET CALCULATOR ===")
    payload_b = 24  # Misalnya 11B payload sensor + 13B header LoRaWAN MAC minimum
    bw_hz = 125_000

    print(f"Parameter simulasi: Payload={payload_b} B, BW={bw_hz//1000} kHz, CR=4/5, Preamble=8, CRC=ON")
    print("(Catatan regulasi: duty cycle/dwell time aktual wajib merujuk LoRa Alliance RP2 & regulator nasional.)\n")
    print(f"{'SF':>4} | {'T_sym (ms)':>10} | {'DE':>2} | {'ToA (ms)':>10} | {'Contoh 1% Wait (s)':>18} | {'Sens_SX1276 (dBm)':>17}")
    print("-" * 76)

    for sf in range(7, 13):
        t_sym, toa_ms, de = lora_time_on_air_ms(sf=sf, bw_hz=bw_hz, payload_bytes=payload_b)
        wait_1pct_s = (toa_ms * 99.0) / 1000.0
        sens = TYPICAL_SENSITIVITY_DBM_BW125[sf]
        print(f"SF{sf:<2} | {t_sym:10.3f} | {de:2d} | {toa_ms:10.2f} | {wait_1pct_s:18.2f} | {sens:17.1f}")

    # Contoh Link Budget untuk skenario 3 km pada pita uji 923 MHz (hanya model propagasi FSPL + rugi fading)
    p_tx_dbm = 14.0
    g_tx_dbi = 2.0
    g_rx_dbi = 3.0
    cable_loss_db = 1.5
    shadow_margin_db = 15.0
    dist_km = 3.0
    freq_mhz = 923.0
    loss_fspl = fspl_db(dist_km, freq_mhz)
    p_rx_dbm = p_tx_dbm + g_tx_dbi + g_rx_dbi - cable_loss_db - loss_fspl - shadow_margin_db

    print(f"\n[LINK BUDGET @ {dist_km:.1f} km, {freq_mhz:.0f} MHz, shadow_margin={shadow_margin_db:.0f} dB]")
    print(f"FSPL = {loss_fspl:.2f} dB | P_rx_est = {p_rx_dbm:.2f} dBm")
    for sf in (7, 10, 12):
        margin = p_rx_dbm - TYPICAL_SENSITIVITY_DBM_BW125[sf]
        print(f"  Margin di SF{sf:<2} (sens {TYPICAL_SENSITIVITY_DBM_BW125[sf]:.1f} dBm): {margin:+.2f} dB")


if __name__ == "__main__":
    main()

