# Bukti & Output Eksekusi — Chapter 05

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (simulasi aritmatika *unsigned 32-bit rollover* dan transisi FSM pada Python)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-05/src/fsm_timing_sim.py`
- **Firmware C++ (.ino)**: **Belum diuji** (`arduino-cli`, `wokwi-cli`, dan board ESP32 fisik tidak tersedia pada environment server ini)

## 2. Output Aktual (Verbatim — Software Verification)

```text
=== SIMULASI ROLLOVER millis() & TRANSISI FSM (CHAPTER 05) ===
[PASS] Rollover u32: prev=0xFFFFFFF0, now=0x000003D8 -> elapsed=1000 ms
t=1000 ms | seq=1 | sim_temp=28.4 C -> next_state=IDLE
t=2000 ms | seq=2 | sim_temp=29.3 C -> next_state=IDLE
t=3000 ms | seq=3 | sim_temp=30.2 C -> next_state=ALERT
t=4000 ms | seq=4 | sim_temp=31.1 C -> next_state=ALERT
t=5000 ms | seq=5 | sim_temp=32.0 C -> next_state=ALERT
t=6000 ms | seq=6 | sim_temp=27.0 C -> next_state=IDLE
t=7000 ms | seq=7 | sim_temp=27.9 C -> next_state=IDLE
t=8000 ms | seq=8 | sim_temp=28.8 C -> next_state=IDLE
```

## 3. Expected Serial Monitor Output (Teoretis untuk `ex02_nonblocking_fsm.ino` — Belum Dieksekusi)

```text
=== CHAPTER 05: NON-BLOCKING FSM STARTED ===
[SEQ 1] state=SAMPLE sim_temp=28.4 C
[SEQ 2] state=SAMPLE sim_temp=29.3 C
[SEQ 3] state=SAMPLE sim_temp=30.2 C
...
```

## Verifikasi Kompilasi Arduino ESP32 (Native Toolchain)

- **Toolchain**: `arduino-cli v1.5.1`
- **Core Target**: `esp32:esp32@3.3.12` (Espressif Arduino Core)
- **Target Board (FQBN)**: `esp32:esp32:esp32`
- **Pustaka Tambahan**: `PubSubClient v2.8.0` (pada chapter yang menggunakan MQTT)
- **Tanggal Verifikasi**: 2026-11-11

### Sketsa `ex01_types_serial`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-05/src/ex01_types_serial
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 269032 bytes (20%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22116 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```

### Sketsa `ex02_nonblocking_fsm`

Perintah kompilasi:
```bash
arduino-cli compile --fqbn esp32:esp32:esp32 public/content/chapter-05/src/ex02_nonblocking_fsm
```

Hasil kompilasi aktual:
```text
EXIT=0
Sketch uses 272284 bytes (20%) of program storage space. Maximum is 1310720 bytes.
Global variables use 22156 bytes (6%) of dynamic memory, leaving local variables. Maximum is 327680 bytes.
```
