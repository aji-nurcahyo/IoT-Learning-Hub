# Bukti & Output Eksekusi — Chapter 01

## 1. Informasi Lingkungan Pengujian

- **Jenis verifikasi**: `software` (simulasi alur data IoT berbasis dataset sintetis)
- **Tanggal**: 2026-11-10
- **Environment**: Windows, Python 3.12.10
- **Perintah**: `python public/content/chapter-01/src/iot_flow_demo.py`
- **Hardware fisik**: Tidak digunakan (belum relevan pada chapter fondasi konseptual)

## 2. Output Aktual (Verbatim)

```text
=== SIMULASI ALUR DATA END-TO-END IoT (DATA SINTETIS) ===
Sumber dataset: telemetry.csv (synthetic)
--------------------------------------------------------------------
[PLATFORM OK ] {"device_id": "gh-node-01", "seq": 1, "temp_c": 27.4, "humidity_pct": 68.2, "source": "synthetic", "downlink_command": "FAN_OFF"}
[PLATFORM OK ] {"device_id": "gh-node-01", "seq": 2, "temp_c": 28.9, "humidity_pct": 65.5, "source": "synthetic", "downlink_command": "FAN_OFF"}
[PLATFORM OK ] {"device_id": "gh-node-01", "seq": 3, "temp_c": 30.6, "humidity_pct": 61.0, "source": "synthetic", "downlink_command": "FAN_ON"}
[PLATFORM OK ] {"device_id": "gh-node-01", "seq": 4, "temp_c": 31.2, "humidity_pct": 59.4, "source": "synthetic", "downlink_command": "FAN_ON"}
[GATEWAY DROP] seq=5 dev=gh-node-01 alasan=temp_c=125.0 di luar rentang sensor (-40..85 C)
[PLATFORM OK ] {"device_id": "gh-node-01", "seq": 6, "temp_c": 29.1, "humidity_pct": 63.8, "source": "synthetic", "downlink_command": "FAN_OFF"}
--------------------------------------------------------------------
Ringkasan: diterima=5, ditolak=1, total=6
```

## 3. Catatan Keterbatasan

Output di atas memvalidasi logika penyaringan payload dan aturan kendali sederhana menggunakan data sintetis (`telemetry.csv`). Pengujian ini **tidak** mengukur performa radio nirkabel, delay jaringan nyata, atau akurasi sensor fisik.

