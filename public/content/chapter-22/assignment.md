# Tugas Mandiri: Rancang Bangun Edge Gateway Daemon & Layanan systemd

## Deskripsi Tugas

Tugas ini menguji kompetensi mahasiswa dalam merancang program gerbang perantara (*edge gateway*) yang andal pada sistem operasi Linux Raspberry Pi. Anda diminta untuk mengintegrasikan pembacaan data serial dari mikrokontroler, memvalidasi integritas frame berbasis *checksum*, mempublikasikan data ke broker MQTT lokal, dan mengonfigurasikan unit layanan `systemd` dengan prinsip keamanan *least privilege*.

## Petunjuk Pengerjaan

1. **Pemrograman Gateway Daemon**:
   - Implementasikan kelas `SerialMqttGateway` yang membaca stream karakter baris demi baris secara non-blocking.
   - Ekstrak token identitas perangkat, nomor sekuens, nilai metrik sensor, dan voltase baterai dari frame berpenanda `$DATA,...*CS`.
   - Tolak dan catat setiap frame yang memiliki panjang token tidak sesuai atau gagal verifikasi *checksum*.
2. **Penanganan Sinyal POSIX**:
   - Daftarkan penangan sinyal (*signal handler*) untuk `SIGINT` dan `SIGTERM`.
   - Pastikan variabel kontrol loop diubah secara aman saat sinyal diterima, dan cetak statistik total paket sukses serta korup sebelum program keluar.
3. **Konfigurasi Unit Layanan `systemd`**:
   - Susun file unit `iot-gateway.service` yang menjalankan program gateway di bawah user non-root `iotgateway`.
   - Terapkan kebijakan pemulihan otomatis (`Restart=always`), interval jeda (`RestartSec=5s`), serta batasan hak akses sistem (`ProtectSystem=full`).
4. **Verifikasi dan Pengujian**:
   - Jalankan skrip pengujian mandiri menggunakan mock stream yang memuat variasi frame valid, frame dengan checksum salah, dan frame derau (*noise*).
   - Lampirkan log keluaran eksekusi terminal dan dokumentasikan analisis ketahanan program.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :---: | :--- | :---: | :--- |
| 1 | **Protokol Framing & Integritas Checksum** | 40 | Gateway mampu mem-parse struktur frame serial dengan benar dan menolak data korup/noise secara konsisten melalui verifikasi LRC. |
| 2 | **Graceful Shutdown & Penanganan Sinyal** | 30 | Daemon merespons sinyal terminasi sistem operasi tanpa menimbulkan resource leak atau proses zombie di memori. |
| 3 | **Konfigurasi systemd & Penguatan Keamanan** | 30 | File unit systemd terkonfigurasi lengkap dengan hak akses non-root, sandboxing direktori sistem, dan parameter supervisi pemulihan otomatis. |
