# Bukti & Output Eksekusi — Chapter 08

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (kalibrasi dua titik dan propagasi ketidakpastian *Type A + Type B* pada dataset referensi sintetis `telemetry.csv`)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-08/src/calibration_uncertainty.py`
- **Firmware ESP32 (.ino)**: **Belum diuji** (`arduino-cli`, `wokwi-cli`, dan termistor fisik tidak tersedia pada environment server ini)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== ANALISIS KALIBRASI & KETIDAKPASTIAN PENGUKURAN (CHAPTER 08) ===
Dataset sintetis: telemetry.csv (source=synthetic)
Titik kalibrasi : Low=(1.42 -> 0.00 C), High=(59.22 -> 60.00 C)
Model kalibrasi : T_cal = 1.0381 * T_raw + (-1.4740)
RMSE sebelum kalibrasi : 0.8544 C
RMSE sesudah kalibrasi : 0.0266 C

--- Evaluasi Ketidakpastian pada Titik Referensi 25.00 C (n=5) ---
Rata-rata terkalibrasi : 25.046 C (Std Dev s = 0.0495 C)
u_A (random mean)      : 0.0221 C
u_B (ref +-0.10 C)     : 0.0577 C
u_B (resolusi 0.05 C)  : 0.0144 C
u_c (gabungan)         : 0.0635 C
Hasil lapor (k=2, 95%) : 25.05 +/- 0.13 C
```

## 3. Expected Serial Monitor Output (Teoretis untuk `ex01_ntc_calibrated.ino` — Belum Dieksekusi)

```text
=== CHAPTER 08: NTC SENSOR ACQUISITION & TWO-POINT CALIBRATION ===
n=10 raw_mean=25.55 C cal_temp=25.05 C s=0.049 C uA=0.015 C
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `ex01_ntc_calibrated`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-08/src/ex01_ntc_calibrated
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 279396 bytes (21%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22196 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
