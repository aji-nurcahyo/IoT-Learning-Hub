# Tugas & Rubrik — Chapter 10 (Embedded Foundations Capstone)

## Proyek Akhir Level 1: Smart Environmental Monitoring & Local Control System

Bangun dan dokumentasikan sistem kendali lingkungan lokal berbasis `ESP32-DevKitC V4` (jalur **Path A Simulasi Wokwi + Python** atau **Path B Hardware Fisik Low-Voltage DC Opsional**). Wi-Fi, MQTT, dan *Cloud* **tidak** diwajibkan pada proyek ini.

## Spesifikasi Minimal Proyek

1. **Sensing & Kalibrasi**: 1 input analog (`ADC1`) dengan *moving average* non-blocking, kalibrasi linier/Beta, dan deteksi kerusakan sensor (`NaN`).
2. **Input Digital & Interlock**: 1 tombol mode ter-*debounce* ($\ge 3$ mode termasuk pilihan ambang histeresis) dan 1 *safety interlock* darurat.
3. **Actuator & Control**: Output PWM (`LEDC`) untuk kipas/indikator beban, LED status mode, dan buzzer alarm *fail-safe*.
4. **Serial Telemetry**: Output terstruktur JSON setiap 1 detik (`115200 baud`) memakai buffer statis (`snprintf`).
5. **Pengujian Sistematis**: Jalankan minimal 7 *Test Cases* (normal, *deadband* histeresis, pergantian mode, *interlock*, dan *sensor fault*).

## Template Laporan Teknis Capstone

Kumpulkan paket kode (`.ino`, `.h`, `wokwi_diagram.json` / skrip uji) beserta laporan teknis (4–8 halaman) berstruktur berikut:
1. **Ringkasan Sistem & Requirements** (Fungsional & Non-Fungsional terukur)
2. **Arsitektur, Bill of Materials (BOM) & Wiring Table** (*low-voltage DC* + *common GND* + proteksi driver)
3. **Desain Firmware & Kalibrasi** (Diagram FSM, parameter kalibrasi & histeresis)
4. **Rencana & Hasil Pengujian** (Tabel *Test Case ID | Kondisi | Expected | Actual | Pass/Fail* + salinan log asli)
5. **Status Verifikasi, Keterbatasan & Keselamatan** (nyatakan jujur: *Belum diuji / Compile-verified / Simulator-verified / Hardware-verified*)

## Rubrik Penilaian Capstone (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Arsitektur, BOM & keselamatan wiring DC** | **20** | Diagram arsitektur lengkap, BOM realistis, pin mapping valid, serta driver MOSFET/flyback & *common GND* benar. |
| **Akuisisi terkalibrasi & kontrol histeresis** | **25** | Pembacaan `ADC1` terfilter *moving average*, kalibrasi terdokumentasi, dan histeresis mencegah *chattering*. |
| **Firmware non-blocking, FSM & fail-safe** | **25** | Kode modular `.h`/`.ino`, bebas `delay()` di `loop()`, *debounce* tombol akurat, serta *interlock* & fault `NaN` aman. |
| **Pengujian test-case, dokumentasi & kejujuran** | **30** | Minimal 7 skenario uji dijalankan dan dicatat lengkap (*Expected vs Actual*) dengan status verifikasi sesuai bukti nyata. |

