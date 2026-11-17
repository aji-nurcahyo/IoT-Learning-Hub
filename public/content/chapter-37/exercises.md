# Latihan Chapter 37: Scalable IoT Architecture & Deployment

## Latihan Konseptual

1. **Komparasi Scale-Up vs Scale-Out**:
   Bandingkan pendekatan *Vertical Scaling* (menambah spesifikasi satu server) dengan *Horizontal Scaling* (menambah node kluster komoditas) untuk platform IoT yang melayani 500.000 perangkat. Analisis berdasarkan: batas kapasitas fisik perangkat keras, ketersediaan tinggi (*High Availability*), dan efisiensi biaya infrastruktur.

2. **Dinamika Sharding & Hash Key Selection**:
   Mengapa dalam arsitektur partisi antrean IoT (seperti Kafka atau kluster MQTT), identitas perangkat (*Device ID*) wajib digunakan sebagai kunci hash partisi alih-alih jenis sensor atau stempel waktu (*timestamp*)? Jelaskan hubungannya dengan jaminan urutan data (*in-order processing*).

3. **Mekanisme Backpressure Pushback vs Dropping**:
   Jelaskan perbedaan mendasar antara kebijakan *Pushback / Throttling* (pelambatan laju sampling di edge) dengan kebijakan *Drop Oldest / Drop Newest* di backend saat terjadi kemacetan antrean database. Kapan masing-masing strategi tepat untuk diterapkan?

## Latihan Praktik & Perhitungan

1. **Kalkulasi Distribusi Partisi Hash MD5**:
   Diberikan kluster dengan 4 partisi antrean (Partisi 0, 1, 2, 3).
   - Tuliskan fungsi Python sederhana yang menghitung indeks partisi dari string identitas `dev-sensor-42`.
   - Jelaskan mengapa output fungsi hash kriptografi (seperti MD5 atau SHA-256) menghasilkan distribusi nilai modulo yang seragam (*uniform distribution*) bahkan ketika nama identitas perangkat hanya berbeda satu angka berurutan.

2. **Analisis Batas Soket & Tuning Kernel Linux**:
   Sebuah server Ubuntu Linux dialokasikan untuk menjalankan broker EMQX dengan target 200.000 koneksi TCP simultan.
   - Mengapa konfigurasi default `fs.file-max` dan `nofile` (biasanya 1024) menyebabkan penolakan koneksi massal?
   - Tuliskan baris konfigurasi file `/etc/security/limits.conf` dan `/etc/sysctl.conf` yang diperlukan untuk membuka alokasi hingga 500.000 file descriptor.
