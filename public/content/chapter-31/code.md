# Panduan Implementasi: Low-Power Design & Energy Measurement

Dokumen ini menjelaskan implementasi skrip pemodelan konsumsi daya Python dan kode firmware C++ ESP32 Arduino Core untuk mode *deep sleep*.

## 1. Skrip Pemodelan Konsumsi Daya Python

Skrip [power_model_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-31/src/power_model_sim.py) memodelkan konsumsi muatan listrik berkala:

```python
def calculate_average_current(
    active_current_ma: float,
    active_time_s: float,
    sleep_current_ua: float,
    sleep_time_s: float,
) -> float:
    total_time_s = active_time_s + sleep_time_s
    sleep_current_ma = sleep_current_ua / 1000.0
    charge_mas = (active_current_ma * active_time_s) + (sleep_current_ma * sleep_time_s)
    return charge_mas / total_time_s
```

Untuk menjalankan simulasi secara lokal:

```bash
python public/content/chapter-31/src/power_model_sim.py
```

### Karakteristik Tiga Skenario Pengujian:
1. **Skenario 1 (Agresif - Interval 60 Detik)**: $I_{avg} = 3.01\text{ mA}$, estimasi baterai 2500 mAh bertahan sekitar 29.4 hari.
2. **Skenario 2 (Konservatif - Interval 600 Detik / 10 Menit)**: $I_{avg} = 0.31\text{ mA}$, estimasi baterai bertahan sekitar 285.6 hari (~0.78 tahun).
3. **Skenario 3 (Sensor Gating - Interval 1800 Detik / 30 Menit)**: $I_{avg} = 0.027\text{ mA}$, estimasi baterai bertahan hingga 3252.7 hari (~8.75 tahun).

## 2. Firmware ESP32 Deep Sleep C++

Firmware [esp32_low_power_firmware.ino](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-31/src/esp32_low_power_firmware.ino) mendemonstrasikan:
- Penggunaan variabel persisten `RTC_DATA_ATTR int bootCount = 0;` yang tidak hilang saat CPU utama dimatikan.
- Identifikasi sumber pemicu bangun melalui `esp_sleep_get_wakeup_cause()`.
- Penjadwalan alarm RTC internal melalui `esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR)`.
- Pemanggilan `Serial.flush()` sebelum `esp_deep_sleep_start()` untuk menjamin buffer transmisi UART terkirim bersih sebelum clock dihentikan.
