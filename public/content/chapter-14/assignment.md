# Tugas & Rubrik — Chapter 14

## Skenario Tugas: Rancangan Hierarki Topic & Protokol Pub/Sub Sistem Smart Campus

Rancang sistem pertukaran pesan MQTT lokal untuk **3 gedung kampus**, masing-masing memiliki 2 ruang lab yang memantau `temp_c` dan `humidity_pct` serta memiliki aktuator `fan` (`ON`/`OFF`).

## Instruksi Pengerjaan

1. **Desain Hierarki Topic & Wildcard**: Susun tabel topic *uplink* (*telemetry*) dan *downlink* (*command*) yang konsisten tanpa *leading slash*, serta tuliskan minimal 3 contoh pola *subscribe* menggunakan `+` dan `#` beserta deskripsi pesan yang tertangkap.
2. **Desain Payload JSON & Keamanan Mosquitto**: Definisikan format payload JSON (memuat `device_id`, `seq`, satuan eksplisit) dan tuliskan draf `mosquitto.conf` lokal yang menerapkan autentikasi (`allow_anonymous false`) serta batas akses jaringan.
3. **Implementasi Klien / Simulasi**: Sesuaikan `mqtt_pubsub_client.ino` (dengan `clientId` unik, `setBufferSize()`, `mqtt.loop()`) dan jalankan uji simulasi loopback (`mqtt_broker_sim.py` atau Mosquitto lokal jika tersedia) dengan pelaporan bukti yang jujur.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Desain hierarki topic & aturan wildcard** | **25** | Topic konsisten tanpa leading `/`, bebas wildcard di publish, dan penggunaan `+`/`#` tepat. |
| **Desain skema payload JSON & keamanan broker** | **25** | Payload ringkas berunit eksplisit serta konfigurasi Mosquitto aman (tanpa anonymous publik). |
| **Implementasi klien Pub/Sub non-blocking** | **30** | `clientId` unik, `mqtt.loop()`, buffer memadai, dan callback kendali bersih tanpa `delay()`. |
| **Pengujian loopback/broker & kejujuran bukti** | **20** | Hasil uji pub-sub terdokumentasi jelas beserta status verifikasi aktual. |

