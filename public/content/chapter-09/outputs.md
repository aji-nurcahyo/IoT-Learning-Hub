# Bukti & Output Eksekusi — Chapter 09

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (simulasi kontrol *single-threshold* vs *hysteresis* dan skenario *fail-safe* sensor `NaN` pada `telemetry.csv`)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-09/src/hysteresis_control_sim.py`
- **Firmware ESP32 (.ino)**: **Belum diuji** (`arduino-cli`, `wokwi-cli`, dan rangkaian driver fisik tidak tersedia pada environment server ini)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== SIMULASI KONTROL HISTERESIS & FAIL-SAFE (CHAPTER 09) ===
step= 1 | temp=29.60 C | fan=OFF
step= 2 | temp=29.90 C | fan=OFF
step= 3 | temp=30.10 C | fan=ON 
step= 4 | temp=29.80 C | fan=ON 
step= 5 | temp=30.20 C | fan=ON 
step= 6 | temp=29.70 C | fan=ON 
step= 7 | temp=30.10 C | fan=ON 
step= 8 | temp=29.90 C | fan=ON 
step= 9 | temp=30.30 C | fan=ON 
step=10 | temp=29.40 C | fan=ON 
step=11 | temp=28.70 C | fan=ON 
step=12 | temp=28.10 C | fan=ON 
step=13 | temp=27.80 C | fan=OFF
step=14 | temp=28.20 C | fan=OFF
step=15 | temp=28.60 C | fan=OFF
step=16 | temp=  NaN | STATUS=FAIL_SAFE_OFF (Alarm ON)
------------------------------------------------------------
Jumlah transisi (Single-Threshold 30.0 C) : 8 kali (CHATTERING!)
Jumlah transisi (Histeresis 28.0..30.0 C) : 2 kali (STABIL)
```

## 3. Expected Serial Monitor Output (Teoretis untuk `ex01_hysteresis_driver.ino` — Belum Dieksekusi)

```text
=== CHAPTER 09: HYSTERESIS CONTROL + INTERLOCK + FAIL-SAFE ===
temp=29.50 C | fan=OFF | duty=0/255 | interlock=OK
temp=30.40 C | fan=ON | duty=204/255 | interlock=OK
[FAIL-SAFE] Kipas OFF, Alarm ON | Alasan: SAFETY_INTERLOCK_OPEN
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `ex01_hysteresis_driver`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-09/src/ex01_hysteresis_driver
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 289171 bytes (22%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22392 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
