# Bukti & Output Eksekusi — Chapter 07

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (simulasi kuantisasi 12-bit, *moving average* pada `telemetry.csv`, dan pembuktian *aliasing* Nyquist di Python)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-07/src/adc_nyquist_sim.py`
- **Firmware ESP32 (.ino)**: **Belum diuji** (`arduino-cli`, `wokwi-cli`, dan board ESP32 fisik tidak tersedia pada environment server ini)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== SIMULASI ADC, FILTERING & NYQUIST ALIASING (CHAPTER 07) ===
1. ADC 12-bit (V_FS=3.30 V): 4096 level, 1 LSB = 0.8059 mV
   Ketidakpastian kuantisasi ideal = +/-0.4029 mV

2. Uji Moving Average (N=4) pada telemetry.csv (true_mv=1650.0 mV):
   Std dev mentah          : 21.32 mV
   Std dev setelah filter  : 2.30 mV
   Rata-rata akhir terfilter: 1653.02 mV

3. Uji Nyquist: f_sig=60 Hz, f_s=80 Hz (< 2*f_sig = 120 Hz)
   Frekuensi alias terhitung : 20.0 Hz
   Deviasi sampel 60Hz vs -sin(20Hz): 1.41e-14 (identik secara diskrit!)
```

## 3. Expected Serial Monitor Output (Teoretis untuk `ex01_adc_pwm_dimmer.ino` — Belum Dieksekusi)

```text
=== CHAPTER 07: ADC1 MOVING AVERAGE + LEDC PWM ===
raw_mv=1642 avg_mv=1650 duty=511/1023 (50.0%)
raw_mv=1661 avg_mv=1652 duty=512/1023 (50.0%)
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `ex01_adc_pwm_dimmer`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-07/src/ex01_adc_pwm_dimmer
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 286723 bytes (21%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22440 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
