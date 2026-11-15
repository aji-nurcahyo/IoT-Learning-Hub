# Panduan Implementasi Kode — Chapter 24

Dokumentasi ini menjelaskan konfigurasi alur pada berkas [`flows.json`](content/chapter-24/src/flows.json) dan mesin simulator pada skrip [`nodered_flow_runner.py`](content/chapter-24/src/nodered_flow_runner.py).

## Struktur Berkas flows.json

Alur disusun secara modular dalam bentuk larik objek JSON deklaratif:

1. **`node_mqtt_in`**:
   Mendengarkan topik `iot/lab/+/telemetry` dengan format payload otomatis diurai sebagai `json`. Mengalirkan kawat ke `node_switch_filter` dan `node_save_context`.
2. **`node_save_context`**:
   Simpul tipe `change` yang mengeksekusi aturan:
   - Target: `global.latest_telemetry`
   - Sumber: `msg.payload`
3. **`node_switch_filter`**:
   Mengevaluasi `msg.payload.metrics.temp_c`:
   - Port 1: `>= 30.0` (dihubungkan ke `node_alarm_enricher`)
   - Port 2: `< 30.0` (dihubungkan ke `node_normal_log`)
4. **`node_alarm_enricher`**:
   Menyusun struktur objek alarm baru berbasis JavaScript dan menetapkan topik terbitan `iot/lab/{dev}/event/alarm`.
5. **`node_http_in` & `node_http_response`**:
   Membuka jalur API REST mikro pada rute `GET /api/v1/telemetry/latest` yang membaca konteks global dan mengembalikan data dalam format JSON.
6. **`node_catch_error`**:
   Menangkap setiap kesalahan runtime tanpa merusak alur eksekusi canvas.

## Eksekusi Pengujian Simulator

Jalankan skrip runner untuk memverifikasi alur tanpa memerlukan instalasi Node.js eksternal:

```bash
python public/content/chapter-24/src/nodered_flow_runner.py
```
