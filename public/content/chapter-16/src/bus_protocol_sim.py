"""Kalkulator & Simulasi Parameter Bus Serial: UART, I2C & SPI (Chapter 16).

Menghitung dan memvalidasi:
1. Efisiensi frame UART (8N1 = 10 bit/byte vs 8E1 = 11 bit/byte) dan laju payload maksimum.
2. Evaluasi rise-time pull-up I2C (t_r = 0.8473 * R_p * C_bus) terhadap batas Standard Mode (100 kHz, <= 1000 ns)
   dan Fast Mode (400 kHz, <= 300 ns), serta cek tabrakan alamat 7-bit.
3. Tabel perbandingan Mode SPI (0..3: CPOL/CPHA) dan durasi transfer frame SPI 4 MHz.
"""

from __future__ import annotations


def analyze_uart(baud: int, data_bits: int = 8, parity_bits: int = 0, stop_bits: int = 1) -> None:
    bits_per_frame = 1 + data_bits + parity_bits + stop_bits
    eff = data_bits / bits_per_frame
    max_bytes_per_s = baud / bits_per_frame
    print(
        f"UART {baud} baud ({data_bits}{'N' if parity_bits == 0 else 'E'}{stop_bits}): "
        f"{bits_per_frame} bit/frame -> efisiensi={eff*100:.1f}%, maks={max_bytes_per_s:,.0f} B/s"
    )


def analyze_i2c_pullup(r_pullup_ohm: float, c_bus_pf: float) -> None:
    # Sesuai datasheet NXP UM10204: t_r ~= 0.8473 * R_p * C_bus (untuk ambang 30%-70% VDD)
    t_r_ns = 0.8473 * r_pullup_ohm * (c_bus_pf * 1e-12) * 1e9
    ok_100k = t_r_ns <= 1000.0
    ok_400k = t_r_ns <= 300.0
    print(
        f"I2C R_p={r_pullup_ohm:.0f} ohm, C_bus={c_bus_pf:.0f} pF -> t_r={t_r_ns:.1f} ns | "
        f"100kHz(<=1000ns)={ok_100k} | 400kHz(<=300ns)={ok_400k}"
    )


def main() -> None:
    print("=== ANALISIS TEKNIS UART, I2C & SPI (CHAPTER 16) ===")
    analyze_uart(9600, 8, 0, 1)
    analyze_uart(115200, 8, 0, 1)
    analyze_uart(115200, 8, 1, 1)

    print("\n--- Evaluasi Pull-Up I2C (Batas NXP UM10204) ---")
    analyze_i2c_pullup(10000, 100)  # 10 kOhm terlalu lemah untuk 400 kHz!
    analyze_i2c_pullup(4700, 100)   # 4.7 kOhm standar
    analyze_i2c_pullup(2200, 100)   # 2.2 kOhm aman hingga 400 kHz

    print("\n--- Cek Konflik Alamat I2C 7-bit ---")
    devices = {"BME280": 0x76, "OLED_SSD1306": 0x3C, "BMP280_alt": 0x76}
    seen: dict[int, str] = {}
    for name, addr in devices.items():
        if addr in seen:
            print(f"  [KONFLIK] {name} (0x{addr:02X}) bentrok dengan {seen[addr]}! Ubah pin SDO/ADDR atau pakai I2C mux.")
        else:
            seen[addr] = name

    print("\n--- Matriks Mode SPI & Waktu Transfer 64 Byte @ 4 MHz ---")
    spi_modes = [(0, 0, 0), (1, 0, 1), (2, 1, 0), (3, 1, 1)]
    for m, cpol, cpha in spi_modes:
        edge = "Rising" if (cpol == cpha) else "Falling"
        print(f"  SPI_MODE{m}: CPOL={cpol}, CPHA={cpha} -> sample data pada {edge} edge")
    xfer_us = (64 * 8) / 4.0  # 4 MHz = 4 bit/us
    print(f"  Durasi transfer 64 byte SPI @ 4 MHz = {xfer_us:.1f} us (vs ~5.56 ms pada UART 115200)")


if __name__ == "__main__":
    main()

