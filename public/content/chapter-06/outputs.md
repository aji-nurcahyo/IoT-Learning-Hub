# Bukti & Output Eksekusi — Chapter 06

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (simulasi algoritma *software debouncing* pada aliran sampel *switch bounce* sintetis `telemetry.csv`)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-06/src/debounce_sim.py`
- **Firmware ESP32 (.ino)**: **Belum diuji** (`arduino-cli`, `wokwi-cli`, dan board ESP32 fisik tidak tersedia pada environment server ini)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== SIMULASI SWITCH BOUNCE & DEBOUNCE FSM (CHAPTER 06) ===
Dataset sintetis: telemetry.csv (23 sampel, 2 tekan fisik ber-bounce)
1) Naive falling-edge (tanpa debounce) : 6 kali terpicu (SALAH - bounce terhitung!)
2) Software debounce (T_db=50 ms)      : 2 kali terpicu (BENAR)
   [PRESS #1] t=90 ms -> LED Mode = ON
   [PRESS #2] t=310 ms -> LED Mode = BLINK
```

## 3. Expected Serial Monitor Output (Teoretis untuk `ex01_button_debounce_fsm.ino` — Belum Dieksekusi)

```text
=== CHAPTER 06: DEBOUNCE + EDGE DETECT + LED FSM ===
Mode awal: OFF (tekan tombol di GPIO 27 untuk beralih mode)
[PRESS #1] t=1420 ms -> LED Mode = ON
[PRESS #2] t=3890 ms -> LED Mode = BLINK
[PRESS #3] t=7110 ms -> LED Mode = OFF
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `ex01_button_debounce_fsm`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-06/src/ex01_button_debounce_fsm
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 272400 bytes (20%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22132 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```

### Sketsa `ex02_interrupt_flag`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-06/src/ex02_interrupt_flag
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 274336 bytes (20%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22612 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
