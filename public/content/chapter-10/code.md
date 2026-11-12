# Source Code — Chapter 10 Capstone: Smart Environmental Monitoring & Local Control

Folder `src/` berisi paket *Firmware* dan simulasi lengkap untuk proyek akhir Level 1:

1. [env_config.h](content/chapter-10/src/capstone_env_monitor/env_config.h): Header konfigurasi pin `ESP32-DevKitC V4`, konstanta kalibrasi NTC, preset histeresis (`AUTO_NORMAL`, `AUTO_STRICT`), dan `enum class ControlMode`.
2. [capstone_env_monitor.ino](content/chapter-10/src/capstone_env_monitor/capstone_env_monitor.ino): Firmware non-blocking terpadu (*moving average* ADC1, kalibrasi 2-titik, *debounce* tombol mode, *safety interlock*, kontrol histeresis PWM, dan *telemetry* JSON Serial 1 Hz).
3. [wokwi_diagram.json](content/chapter-10/src/wokwi_diagram.json): Konfigurasi simulator Wokwi lengkap (`board-esp32-devkit-c-v4` + NTC + Push Button + Slide Switch Interlock + 2 LED + Buzzer).
4. [capstone_logic_test.py](content/chapter-10/src/capstone_logic_test.py) & [telemetry.csv](content/chapter-10/telemetry.csv): *Acceptance test harness* Python yang menguji 12 skenario transisi mode, histeresis, dan *fail-safe*.

## Cara Menjalankan

**Acceptance Test Harness (Python — Software Verification):**
```sh
python public/content/chapter-10/src/capstone_logic_test.py
```

**Firmware ESP32 (Wokwi / Arduino IDE 2.x):**
- Pastikan `capstone_env_monitor.ino` dan `env_config.h` berada di direktori proyek yang sama (atau dua tab pada Wokwi).
- Target board: `ESP32 Dev Module`, board package Arduino-ESP32 v3.x, baud rate `115200`.

