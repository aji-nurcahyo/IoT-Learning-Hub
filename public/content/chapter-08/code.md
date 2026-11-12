# Source Code — Chapter 08: Sensor NTC, Kalibrasi Dua Titik & Ketidakpastian

Folder `src/` berisi:

1. [ex01_ntc_calibrated.ino](content/chapter-08/src/ex01_ntc_calibrated/ex01_ntc_calibrated.ino): Sketsa ESP32 membaca termistor NTC 10k melalui `ADC1` (`GPIO 34`), menghitung suhu dengan persamaan Beta, menerapkan parameter kalibrasi `CAL_SLOPE` & `CAL_OFFSET`, serta menghitung rata-rata dan *standard uncertainty* ($u_A$) dari 10 sampel.
2. [wokwi_diagram.json](content/chapter-08/src/wokwi_diagram.json): Konfigurasi Wokwi (`board-esp32-devkit-c-v4` + modul sensor NTC pada `GPIO 34`).
3. [calibration_uncertainty.py](content/chapter-08/src/calibration_uncertainty.py) & [telemetry.csv](content/chapter-08/telemetry.csv): Skrip Python untuk menghitung regresi kalibrasi dua titik, RMSE sebelum/sesudah kalibrasi, serta ketidakpastian gabungan (*Type A* + *Type B*).

## Cara Menjalankan

**Simulasi & Kalkulasi Python (Software Verification):**
```sh
python public/content/chapter-08/src/calibration_uncertainty.py
```

**Firmware ESP32 (Wokwi / Arduino IDE 2.x):**
- Gunakan `ESP32-DevKitC V4`, baud rate `115200`. Pada Wokwi, klik sensor NTC saat simulasi berjalan untuk menggeser nilai suhu uji.

