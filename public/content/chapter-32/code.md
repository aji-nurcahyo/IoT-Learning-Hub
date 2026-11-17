# Panduan Implementasi: RTOS, Concurrency & Scheduling

Dokumen ini menjelaskan implementasi teknis penjadwal preemptive FreeRTOS dan penggunaan antrean thread-safe untuk firmware ESP32.

## 1. Modul Simulasi Penjadwal Preemptive Python

Modul [rtos_scheduler_sim.py](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-32/src/rtos_scheduler_sim.py) mengimplementasikan dua komponen verifikasi:
1. `PreemptiveScheduler`: mensimulasikan perpindahan konteks (*context switch*) ketika task berprioritas lebih tinggi memasuki status siap (*ready*).
2. `FreeRTOSQueueSimulator`: memvalidasi batas kapasitas penampungan antrean dan pencatatan metrik data yang terbuang (*dropped items*).

Jalankan pengujian menggunakan:

```bash
python public/content/chapter-32/src/rtos_scheduler_sim.py
```

### Hasil Trace Eksekusi:
```text
T0:TelemetryTx -> T1:TelemetryTx -> T2:SensorSampling -> T3:SafetyWatchdog -> T4:SensorSampling -> T5:TelemetryTx -> T6:TelemetryTx -> T7:IDLE
```
- Pada `T2`, `SensorSampling` (Prioritas 2) merebut CPU dari `TelemetryTx` (Prioritas 1).
- Pada `T3`, `SafetyWatchdog` (Prioritas 3) melakukan preemption terhadap `SensorSampling`.
- Setelah `SafetyWatchdog` selesai pada tick 4, `SensorSampling` melanjutkan sisa eksekusinya sebelum CPU dikembalikan ke `TelemetryTx`.

## 2. Firmware FreeRTOS ESP32 C++

Firmware [esp32_freertos_tasks.ino](file:///d:/Workstation/Repo%20My%20Corses/Internet%20Of%20Things/public/content/chapter-32/src/esp32_freertos_tasks.ino) menyajikan:
- Pola *Producer-Consumer* yang decoupled: `TaskSensor` menyuntikkan data ke `sensorQueue`, sedangkan `TaskTelemetry` mengonsumsi data secara asinkron.
- `xSemaphoreCreateMutex()` melindungi peripheral Serial UART agar tidak terjadi tumpang-tindih karakter (*scrambled output*).
- `xTaskCreatePinnedToCore()` mengunci eksekusi task pada Core 1 untuk menghindari konflik dengan thread radio Wi-Fi sistem.
