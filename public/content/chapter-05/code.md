# Source Code — Chapter 05: Embedded C/C++ Modular & Non-Blocking FSM

Folder `src/` berisi contoh bertahap dari dasar sintaks hingga *Finite State Machine* (FSM) non-blocking:

1. [ex01_types_serial.ino](content/chapter-05/src/ex01_types_serial/ex01_types_serial.ino): Penggunaan tipe data `uint16_t` / `uint32_t`, fungsi, `snprintf` pada buffer statis, dan *Serial debugging*.
2. [led_timer.h](content/chapter-05/src/ex02_nonblocking_fsm/led_timer.h): File *header* modular berisi `struct BlinkTask` dan fungsi pembaruan berbasis `millis()` yang aman terhadap *rollover* 32-bit.
3. [ex02_nonblocking_fsm.ino](content/chapter-05/src/ex02_nonblocking_fsm/ex02_nonblocking_fsm.ino): Firmware penuh menggabungkan *header modular*, dua LED independen (`GPIO 25` & `GPIO 26`), dan FSM 3-state (`IDLE`, `SAMPLE`, `ALERT`).
4. [wokwi_diagram.json](content/chapter-05/src/wokwi_diagram.json): Konfigurasi simulator Wokwi (`board-esp32-devkit-c-v4` + 2 LED + resistor $220\,\Omega$).
5. [fsm_timing_sim.py](content/chapter-05/src/fsm_timing_sim.py): Skrip Python untuk memverifikasi aritmatika *unsigned 32-bit rollover* dan urutan transisi FSM.

## Cara Menjalankan

**Verifikasi Software (Python):**
```sh
python public/content/chapter-05/src/fsm_timing_sim.py
```

**Firmware ESP32 (Wokwi / Arduino IDE 2.x):**
- Letakkan `ex02_nonblocking_fsm.ino` dan `led_timer.h` pada folder proyek yang sama (atau dua tab di Wokwi).
- Pilih target `ESP32 Dev Module`, kompilasi, dan buka Serial Monitor pada `115200 baud`.

