# Panduan Implementasi Kode — Chapter 30

Dokumentasi ini menjelaskan arsitektur integratif dan cara kerja platform capstone pada skrip [`capstone_platform.py`](content/chapter-30/src/capstone_platform.py).

## Struktur Arsitektur Program

Skrip mengintegrasikan enam subsistem rekayasa IoT dalam satu kesatuan runtime mandiri:

1. **`DeviceTwinRegistry` (Chapter 27)**:
   Mengelola inventaris fisik perangkat dan pasangan status *Desired vs Reported state twin* lengkap dengan deteksi penyimpangan (*drift*).
2. **`TopicAclAuthorizer` (Chapter 28)**:
   Menegakkan matriks otorisasi topik MQTT untuk menjamin isolasi akses antar perangkat (*eavesdropping & spoofing protection*).
3. **`EdgeGatewayProcessor` (Chapter 21, 22, 23)**:
   Memvalidasi kontrak JSON Schema, menyaring paket retransmisi duplikat menggunakan cache LRU/TTL, dan meredam fluktuasi statis dengan filter deadband.
4. **`CapstoneTimeSeriesStorage` (Chapter 25)**:
   Mengelola basis data SQLite deret waktu terindeks komposit `(dev_id, ts)`, menjalankan agregasi rollup 1-menit otomatis, dan mengeksekusi pembersihan retensi data lama.
5. **`CapstoneAlertEngine` (Chapter 26)**:
   Mesin status peringatan 4-tahap (`NORMAL`, `PENDING`, `FIRING`, `RESOLVED`) yang dilengkapi pewaktu durasi penahanan $T_{\text{for}} = 5\text{s}$ dan pita histeresis $1{,}0\,^\circ\text{C}$.
6. **`CapstoneOtaManager` (Chapter 29)**:
   Simulator pembaruan firmware Dual-Bank A/B dengan penandatanganan HMAC-SHA256 dan deteksi bootloop untuk memicu pembatalan otomatis (*Automatic Rollback*).

## Eksekusi Pengujian Penerimaan Sistem (SATC)

Jalankan pengujian penerimaan sistem lengkap langsung dari terminal:

```bash
python public/content/chapter-30/src/capstone_platform.py
```
