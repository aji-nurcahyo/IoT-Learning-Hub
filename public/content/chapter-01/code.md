# Source Code — Chapter 01: Simulasi Alur Data End-to-End IoT

Folder `src/` pada chapter ini berisi skrip Python untuk mensimulasikan perjalanan paket telemetry dari sensor (data sintetis) melalui validasi gateway hingga keputusan kendali actuator.

## Ringkasan File

- [iot_flow_demo.py](content/chapter-01/src/iot_flow_demo.py): Skrip Python 3 standar (tanpa library eksternal) untuk membaca [telemetry.csv](content/chapter-01/telemetry.csv), memvalidasi rentang fisik sensor, dan menghasilkan keputusan downlink `FAN_ON` / `FAN_OFF`.
- [telemetry.csv](content/chapter-01/telemetry.csv): Dataset sintetis 6 baris (`source=synthetic`) yang mencakup 1 paket anomali (`temp_c=125.0`) untuk menguji penyaringan gateway.

## Cara Menjalankan (Path A — Software Simulation)

Pastikan Python 3.10+ terpasang, lalu jalankan dari root repositori:

```sh
python public/content/chapter-01/src/iot_flow_demo.py
```

Di Windows PowerShell:

```powershell
python .\public\content\chapter-01\src\iot_flow_demo.py
```

## Status Verifikasi

- **Software simulation (`iot_flow_demo.py`)**: Dieksekusi langsung menggunakan Python 3.12.10; log lengkap tersimpan pada `outputs.md`.
- **Hardware fisik**: Tidak diperlukan pada Chapter 01 (fokus konseptual & alur data).

