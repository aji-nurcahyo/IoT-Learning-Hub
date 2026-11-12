# Bukti & Output — Chapter 20: Connected Device Capstone

- **Status Verifikasi Saat Ini**: Software End-to-End Integration **Terverifikasi (`software`)** melalui loopback HTTP + MQTT 3.1.1 TCP lokal; kompilasi `.ino` (`compile`), simulasi Wokwi (`simulator`), serta uji pada papan ESP32 fisik (`hardware`) belum dijalankan (**Not Tested**) pada tahap penulisan awal modul.
- **Lingkungan Pengujian**: Python `3.12.10` pada Windows 11, berjalan lokal (`127.0.0.1`) tanpa ketergantungan layanan cloud berbayar.

## Output Aktual `capstone_connectivity_test.py`

Command:

```text
python public/content/chapter-20/src/capstone_connectivity_test.py
```

Exit code: `0`

```text
=== CHAPTER 20 CAPSTONE: END-TO-END CONNECTIVITY ACCEPTANCE SUITE ===
[PASS][TC-01] HTTP GET config 200 OK -> temp_high_c=30.0 C, sample_ms=5000
[PASS][TC-02] MQTT LWT armed ('offline') & Retained status='online' delivered to subscriber
[PASS][TC-03] Live JSON telemetry seq=1..2 verified with valid UTC epoch & time_synced=true
[PASS][TC-04] Outage buffering (depth=4) & local fail-safe hysteresis triggered relay=true at 30.80 C
[PASS][TC-05] Offline batch replay complete (stored=6 unique, duplicates_ignored=1)
[PASS][TC-06] Remote CMD temp_high_c=29.0 received & abrupt drop triggered LWT='offline'
=== ALL 6 CAPSTONE ACCEPTANCE TEST CASES PASSED ===
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `connected_env_capstone`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-20/src/connected_env_capstone
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 1045668 bytes (79%) of program storage space. Maximum is 1310720 bytes.
Global variables use 50600 bytes (15%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
