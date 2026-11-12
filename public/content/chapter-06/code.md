# Source Code — Chapter 06: GPIO Digital I/O, Debouncing & Interrupt

Folder `src/` berisi implementasi lengkap kontrol LED berbasis tombol dengan *debouncing* yang benar:

1. [ex01_button_debounce_fsm.ino](content/chapter-06/src/ex01_button_debounce_fsm/ex01_button_debounce_fsm.ino): *Polling* non-blocking dengan `INPUT_PULLUP`, *software debouncing* $50\text{ ms}$, *falling-edge detection*, dan FSM 3-mode LED (`OFF -> ON -> BLINK -> OFF`).
2. [ex02_interrupt_flag.ino](content/chapter-06/src/ex02_interrupt_flag/ex02_interrupt_flag.ino): Pendekatan *hardware interrupt* (`attachInterrupt` dengan `IRAM_ATTR` dan `volatile` flag) tanpa pemanggilan `Serial` di dalam ISR.
3. [wokwi_diagram.json](content/chapter-06/src/wokwi_diagram.json): Konfigurasi simulator Wokwi (`board-esp32-devkit-c-v4`, tombol ber-*bounce* pada `GPIO 27`, LED + resistor $220\,\Omega$ pada `GPIO 25`).
4. [debounce_sim.py](content/chapter-06/src/debounce_sim.py) & [telemetry.csv](content/chapter-06/telemetry.csv): Simulasi Python membandingkan *naive edge-detect* vs *software debouncing* pada aliran sinyal ber-bounce sintetis.

## Cara Menjalankan

**Simulasi Python (Software Verification):**
```sh
python public/content/chapter-06/src/debounce_sim.py
```

**Firmware ESP32 (Wokwi / Arduino IDE 2.x):**
- Gunakan `ESP32-DevKitC V4` (`ESP32 Dev Module`), baud rate Serial Monitor `115200`.
- Pada Wokwi, perhatikan atribut `"bounce": "1"` pada tombol untuk menguji efektivitas kode *debouncing* Anda.

