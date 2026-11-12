# Source Code — Chapter 07: ADC1 Moving Average, LEDC PWM & Nyquist Sim

Folder `src/` berisi:

1. [ex01_adc_pwm_dimmer.ino](content/chapter-07/src/ex01_adc_pwm_dimmer/ex01_adc_pwm_dimmer.ino): Membaca potensiometer via `ADC1` (`GPIO 34`) menggunakan `analogReadMilliVolts()`, menerapkan filter *moving average* 8-sampel, dan mengatur kecerahan LED via `ledcWrite` 10-bit pada `GPIO 25` (API Arduino-ESP32 v3.x).
2. [wokwi_diagram.json](content/chapter-07/src/wokwi_diagram.json): Konfigurasi simulator Wokwi (`board-esp32-devkit-c-v4` + potensiometer pada `GPIO 34` + LED amber & resistor $220\,\Omega$ pada `GPIO 25`).
3. [adc_nyquist_sim.py](content/chapter-07/src/adc_nyquist_sim.py) & [telemetry.csv](content/chapter-07/telemetry.csv): Skrip Python memverifikasi resolusi LSB 12-bit, penurunan simpangan baku oleh *moving average*, dan pembuktian matematis *aliasing* Nyquist ($60\text{ Hz}$ pada $f_s = 80\text{ Hz}$).

## Cara Menjalankan

**Simulasi Python (Software Verification):**
```sh
python public/content/chapter-07/src/adc_nyquist_sim.py
```

**Firmware ESP32 (Wokwi / Arduino IDE 2.x):**
- Gunakan board package `esp32 by Espressif Systems` **v3.0+** (karena menggunakan `ledcAttach(pin, freq, res)`). Jika memakai v2.x, ganti ke pasangan `ledcSetup()` + `ledcAttachPin()`.

