# Bukti & Output Eksekusi — Chapter 10 Capstone

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (*Acceptance Test Harness* Python 13 skenario terhadap model kalibrasi, histeresis, pergantian mode, dan *fail-safe* dari `capstone_env_monitor.ino`)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-10/src/capstone_logic_test.py`
- **Firmware ESP32 (.ino)**: **Belum diuji** (`arduino-cli`, `wokwi-cli`, dan board ESP32 fisik tidak tersedia pada environment server ini)

## 2. Output Aktual (Verbatim — Software Acceptance Test)

```text
=== ACCEPTANCE TEST HARNESS CAPSTONE LEVEL 1 (CHAPTER 10) ===
[PASS #01] {"seq": 1, "uptime_ms": 1000, "temp_c": 24.48, "mode": "AUTO_NORMAL", "fan": "OFF", "alarm": false, "fault": "NONE"}
[PASS #02] {"seq": 2, "uptime_ms": 2000, "temp_c": 30.58, "mode": "AUTO_NORMAL", "fan": "ON", "alarm": false, "fault": "NONE"}
[PASS #03] {"seq": 3, "uptime_ms": 3000, "temp_c": 28.8, "mode": "AUTO_NORMAL", "fan": "ON", "alarm": false, "fault": "NONE"}
[PASS #04] {"seq": 4, "uptime_ms": 4000, "temp_c": 27.05, "mode": "AUTO_NORMAL", "fan": "OFF", "alarm": false, "fault": "NONE"}
[PASS #05] {"seq": 5, "uptime_ms": 5000, "temp_c": 27.92, "mode": "AUTO_STRICT", "fan": "ON", "alarm": false, "fault": "NONE"}
[PASS #06] {"seq": 6, "uptime_ms": 6000, "temp_c": 26.19, "mode": "AUTO_STRICT", "fan": "ON", "alarm": false, "fault": "NONE"}
[PASS #07] {"seq": 7, "uptime_ms": 7000, "temp_c": 24.48, "mode": "AUTO_STRICT", "fan": "OFF", "alarm": false, "fault": "NONE"}
[PASS #08] {"seq": 8, "uptime_ms": 8000, "temp_c": 24.48, "mode": "MANUAL_ON", "fan": "ON", "alarm": false, "fault": "NONE"}
[PASS #09] {"seq": 9, "uptime_ms": 9000, "temp_c": 24.48, "mode": "FAULT_SAFE", "fan": "OFF", "alarm": true, "fault": "INTERLOCK_OPEN"}
[PASS #10] {"seq": 10, "uptime_ms": 10000, "temp_c": 24.48, "mode": "MANUAL_ON", "fan": "ON", "alarm": false, "fault": "NONE"}
[PASS #11] {"seq": 11, "uptime_ms": 11000, "temp_c": null, "mode": "FAULT_SAFE", "fan": "OFF", "alarm": true, "fault": "SENSOR_FAULT_NAN"}
[PASS #12] {"seq": 12, "uptime_ms": 12000, "temp_c": 24.48, "mode": "MANUAL_ON", "fan": "ON", "alarm": false, "fault": "NONE"}
[PASS #13] {"seq": 13, "uptime_ms": 13000, "temp_c": 24.48, "mode": "AUTO_NORMAL", "fan": "OFF", "alarm": false, "fault": "NONE"}
------------------------------------------------------------------------
Hasil Acceptance Test (Software Logic): 13/13 skenario LULUS
```

## 3. Expected Serial Monitor Output (Teoretis untuk `capstone_env_monitor.ino` — Belum Dieksekusi)

```text
=== CAPSTONE LEVEL 1: SMART ENV MONITOR & LOCAL CONTROL ===
{"seq":1,"uptime_ms":1000,"temp_c":24.48,"mode":"AUTO_NORMAL","fan":"OFF","alarm":false,"fault":"NONE"}
{"seq":2,"uptime_ms":2000,"temp_c":30.58,"mode":"AUTO_NORMAL","fan":"ON","alarm":false,"fault":"NONE"}
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `capstone_env_monitor`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-10/src/capstone_env_monitor
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 290515 bytes (22%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22472 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
