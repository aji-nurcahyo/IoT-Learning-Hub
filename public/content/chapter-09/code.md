# Source Code — Chapter 09: Driver Aktuator, Kontrol Histeresis & Fail-Safe

Folder `src/` berisi implementasi *low-voltage DC* untuk pengendalian aktuator yang aman:

1. [ex01_hysteresis_driver.ino](content/chapter-09/src/ex01_hysteresis_driver/ex01_hysteresis_driver.ino): Kontrol kipas DC via PWM `LEDC` (`GPIO 25`) dengan jendela histeresis $28{,}0\dots 30{,}0\,^\circ\text{C}$, *safety interlock* (`GPIO 27`), dan *fail-safe shutdown* + alarm (`GPIO 26`) saat sensor putus (`NaN`).
2. [wokwi_diagram.json](content/chapter-09/src/wokwi_diagram.json): Konfigurasi Wokwi (`board-esp32-devkit-c-v4` + potensiometer simulasi suhu + *slide switch* interlock + LED beban + buzzer).
3. [hysteresis_control_sim.py](content/chapter-09/src/hysteresis_control_sim.py) & [telemetry.csv](content/chapter-09/telemetry.csv): Simulasi Python membandingkan jumlah pergantian (*chattering*) antara *single-threshold* dan *hysteresis* beserta perilaku *fail-safe*.

## Cara Menjalankan

**Simulasi Python (Software Verification):**
```sh
python public/content/chapter-09/src/hysteresis_control_sim.py
```

**Firmware ESP32 (Wokwi / Arduino IDE 2.x):**
- Gunakan `ESP32-DevKitC V4`, board package Arduino-ESP32 v3.x, baud rate `115200`.
- Pada rangkaian fisik opsional (Path B), motor/relay 5 V **wajib** dicatu dari sumber 5 V eksternal melalui transistor/MOSFET driver + *flyback diode*, **bukan** langsung dari pin GPIO 3,3 V!

