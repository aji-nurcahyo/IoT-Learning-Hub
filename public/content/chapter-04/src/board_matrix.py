"""Pemeriksa Spesifikasi Varian ESP32 & Validasi Alokasi Pin (Chapter 04).

Memastikan perancang tidak mengasumsikan seluruh varian keluarga ESP32
(ESP32, ESP32-S3, ESP32-C3) memiliki arsitektur, jumlah GPIO, atau aturan
strapping/flash pin yang identik.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Esp32Variant:
    name: str
    cpu_arch: str
    cores: int
    max_mhz: int
    sram_kib: int
    usb_native: bool
    flash_spi_pins: tuple[int, ...]
    strapping_pins: tuple[int, ...]
    input_only_pins: tuple[int, ...]


VARIANTS = {
    "ESP32 (WROOM-32)": Esp32Variant(
        name="ESP32 (WROOM-32)",
        cpu_arch="Xtensa LX6 (32-bit)",
        cores=2,
        max_mhz=240,
        sram_kib=520,
        usb_native=False,
        flash_spi_pins=(6, 7, 8, 9, 10, 11),
        strapping_pins=(0, 2, 5, 12, 15),
        input_only_pins=(34, 35, 36, 39),
    ),
    "ESP32-S3": Esp32Variant(
        name="ESP32-S3",
        cpu_arch="Xtensa LX7 (32-bit + AI vector)",
        cores=2,
        max_mhz=240,
        sram_kib=512,
        usb_native=True,
        flash_spi_pins=(26, 27, 28, 29, 30, 31, 32),
        strapping_pins=(0, 3, 45, 46),
        input_only_pins=(),
    ),
    "ESP32-C3": Esp32Variant(
        name="ESP32-C3",
        cpu_arch="RISC-V RV32IMC (32-bit)",
        cores=1,
        max_mhz=160,
        sram_kib=400,
        usb_native=True,
        flash_spi_pins=(12, 13, 14, 15, 16, 17),
        strapping_pins=(2, 8, 9),
        input_only_pins=(),
    ),
}


def audit_pin_choice(variant_key: str, gpio: int, mode: str) -> str:
    v = VARIANTS[variant_key]
    if gpio in v.flash_spi_pins:
        return f"DITOLAK: GPIO {gpio} pada {v.name} terhubung ke SPI Flash internal!"
    if mode == "OUTPUT" and gpio in v.input_only_pins:
        return f"DITOLAK: GPIO {gpio} pada {v.name} bersifat input-only!"
    if gpio in v.strapping_pins:
        return f"PERINGATAN: GPIO {gpio} adalah strapping pin boot pada {v.name}; pastikan tidak mengganggu boot mode."
    return f"AMAN: GPIO {gpio} ({mode}) valid untuk {v.name}."


def main() -> None:
    print("=== PERBANDINGAN VARIAN ESP32 & AUDIT ALOKASI PIN (CHAPTER 04) ===")
    for v in VARIANTS.values():
        print(
            f"- {v.name}: {v.cpu_arch}, {v.cores} core @ {v.max_mhz} MHz, "
            f"SRAM {v.sram_kib} KiB, USB Native={v.usb_native}, FlashPins={v.flash_spi_pins}"
        )

    print("\n--- Uji Audit Pin Lintas Varian ---")
    test_cases = [
        ("ESP32 (WROOM-32)", 6, "OUTPUT"),
        ("ESP32 (WROOM-32)", 34, "OUTPUT"),
        ("ESP32 (WROOM-32)", 12, "INPUT"),
        ("ESP32 (WROOM-32)", 25, "OUTPUT"),
        ("ESP32-C3", 12, "OUTPUT"),
        ("ESP32-S3", 12, "OUTPUT"),
    ]
    for var_name, pin, mode in test_cases:
        print(f"  [{var_name:16s} | GPIO {pin:2d} | {mode:6s}] -> {audit_pin_choice(var_name, pin, mode)}")


if __name__ == "__main__":
    main()

