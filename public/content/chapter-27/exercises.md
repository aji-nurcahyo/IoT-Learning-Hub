# Latihan Soal & Praktik — Chapter 27

## Bagian A — Soal Konseptual

1. **Perbandingan State Model**:
   Jelaskan mengapa pendekatan *Digital Twin (Desired vs Reported State)* jauh lebih tangguh untuk sistem IoT lapangan dibandingkan model *Direct Remote Procedure Call (RPC)* murni saat mengelola ribuan mikrokontroler dengan koneksi internet yang sering putus-putus.
2. **Configuration Drift Management**:
   Jika operator mengubah konfigurasi interval sampling perangkat dari $10\text{s}$ menjadi $2\text{s}$ pada jam 08:00, tetapi perangkat baru menerima pembaruan tersebut pada jam 11:30 karena mengalami pemadaman listrik lokal:
   - Apa status bendera *drift* antara jam 08:00 hingga 11:30?
   - Apa yang dilakukan mikrokontroler begitu ia kembali menyala dan mendeteksi perbedaan versi konfigurasi?
3. **Mitigasi Serangan Perangkat Bekas**:
   Jelaskan risiko keamanan siber jika sebuah sensor pintar yang telah dilepas dari dinding gedung perkantoran (*decommissioned physical hardware*) dibuang ke tempat sampah tanpa melalui prosedur *crypto-erase* dan pencabutan kredensial registri.

## Bagian B — Soal Praktik Komputasi

1. **Simulasi Transisi Ketersediaan Heartbeat**:
   Menggunakan skrip [`fleet_manager.py`](content/chapter-27/src/fleet_manager.py), sebuah node bernama `node-temp-88` memiliki parameter:
   - `degraded_threshold_sec = 20.0s`
   - `heartbeat_timeout_sec = 45.0s`
   Jika waktu denyut terakhir tercatat pada $t = 100\text{s}$, tentukan status ketersediaan node tersebut pada saat $t = 115\text{s}$, $t = 125\text{s}$, dan $t = 150\text{s}$.
2. **Modifikasi Alur Pendaftaran**:
   Tambahkan atribut `site_location` dan `ip_address` pada kelas `DeviceRecord`. Modifikasi metode `enroll_device` untuk menerima kedua parameter tersebut dan cetak representasi kamus (`to_dict()`) dari node yang terdaftar.
