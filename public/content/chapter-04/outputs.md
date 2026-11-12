# Bukti & Output Eksekusi — Chapter 04

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (audit matriks spesifikasi dan aturan pin lintas varian ESP32 menggunakan Python)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-04/src/board_matrix.py`
- **Firmware / Hardware ESP32**: **Belum diuji** (`arduino-cli`, `wokwi-cli`, dan board ESP32 fisik tidak tersedia pada environment server ini)

## 2. Output Aktual (Verbatim — Software Audit)

```text
=== PERBANDINGAN VARIAN ESP32 & AUDIT ALOKASI PIN (CHAPTER 04) ===
- ESP32 (WROOM-32): Xtensa LX6 (32-bit), 2 core @ 240 MHz, SRAM 520 KiB, USB Native=False, FlashPins=(6, 7, 8, 9, 10, 11)
- ESP32-S3: Xtensa LX7 (32-bit + AI vector), 2 core @ 240 MHz, SRAM 512 KiB, USB Native=True, FlashPins=(26, 27, 28, 29, 30, 31, 32)
- ESP32-C3: RISC-V RV32IMC (32-bit), 1 core @ 160 MHz, SRAM 400 KiB, USB Native=True, FlashPins=(12, 13, 14, 15, 16, 17)

--- Uji Audit Pin Lintas Varian ---
  [ESP32 (WROOM-32) | GPIO  6 | OUTPUT] -> DITOLAK: GPIO 6 pada ESP32 (WROOM-32) terhubung ke SPI Flash internal!
  [ESP32 (WROOM-32) | GPIO 34 | OUTPUT] -> DITOLAK: GPIO 34 pada ESP32 (WROOM-32) bersifat input-only!
  [ESP32 (WROOM-32) | GPIO 12 | INPUT ] -> PERINGATAN: GPIO 12 adalah strapping pin boot pada ESP32 (WROOM-32); pastikan tidak mengganggu boot mode.
  [ESP32 (WROOM-32) | GPIO 25 | OUTPUT] -> AMAN: GPIO 25 (OUTPUT) valid untuk ESP32 (WROOM-32).
  [ESP32-C3         | GPIO 12 | OUTPUT] -> DITOLAK: GPIO 12 pada ESP32-C3 terhubung ke SPI Flash internal!
  [ESP32-S3         | GPIO 12 | OUTPUT] -> AMAN: GPIO 12 (OUTPUT) valid untuk ESP32-S3.
```

## 3. Expected Serial Monitor Output (Teoretis untuk `ch04_board_probe.ino` — Belum Dieksekusi)

> **Catatan Kejujuran**: Output di bawah adalah perkiraan teoretis apabila sketsa dijalankan pada `ESP32-DevKitC V4` (`115200 baud`), **bukan** log hasil kompilasi atau hardware nyata.

```text
=== ESP32 BOARD PROBE (CHAPTER 04) ===
Chip Model      : ESP32-D0WDQ6 (contoh bergantung revisi silikon)
Chip Revision   : 100
CPU Cores       : 2
CPU Freq (MHz)  : 240
Flash Size (MB) : 4.00
Free Heap (KiB) : 312.4
Status LED Pin  : GPIO 25 (output LOW)
[HEARTBEAT] LED=HIGH
[HEARTBEAT] LED=LOW
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `ch04_board_probe`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-04/src/ch04_board_probe
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 273748 bytes (20%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22116 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
