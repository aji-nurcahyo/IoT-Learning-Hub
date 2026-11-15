# Latihan Soal & Praktik — Chapter 30

## Bagian A — Soal Konseptual

1. **Evaluasi Arsitektur Terdistribusi**:
   Tinjau kembali arsitektur platform Capstone Level 3. Mengapa pemisahan tanggung jawab (*Separation of Concerns*) antara subsistem Ingestion/Edge, Storage/Database, Alerting Engine, dan Fleet Registry sangat penting saat sistem harus diskalakan dari puluhan menjadi puluhan ribu perangkat?
2. **Ketahanan Terhadap Kondisi Bencana Jaringan**:
   Uraikan skenario yang terjadi pada platform Capstone jika koneksi jaringan antara simpul sensor lapangan dan broker MQTT terputus total selama 4 jam akibat terputusnya kabel transmisi:
   - Bagaimana simpul lapangan mempertahankan fungsi kendali kritis lokal?
   - Apa yang dilakukan oleh mesin pemonitor detak jantung (*Fleet Heartbeat Monitor*) di sisi server?
   - Bagaimana data pengukuran yang tertahan di-drain dan disinkronkan ke basis data deret waktu saat kabel transmisi tersambung kembali?
3. **Analisis Pertahanan Siber Komprehensif**:
   Jika seorang penyerang berhasil mencuri sebuah mikrokontroler sensor dari tiang lampu kampus dan mencoba menyuntikkan data telemetri palsu atas nama perangkat lain, jelaskan mengapa mekanisme otorisasi ACL Mosquitto dan otentikasi mTLS X.509 berhasil menggagalkan upaya penyerang tersebut.

## Bagian B — Soal Praktik Komputasi

1. **Eksplorasi Skenario Uji SATC-04**:
   Pada skrip [`capstone_platform.py`](content/chapter-30/src/capstone_platform.py), ubah parameter mesin peringatan menjadi:
   - `high_limit = 32.0 C`
   - `hysteresis = 2.0 C`
   - `pending_sec = 10.0s`
   Uji skenario di mana suhu melompat ke $33{,}0\,^\circ\text{C}$ selama 8 detik lalu turun ke $31{,}5\,^\circ\text{C}$. Apakah alarm memicu status `FIRING`? Jelaskan alasannya berdasarkan hasil evaluasi state machine.
2. **Kalkulasi Efisiensi Downsampling Capstone**:
   Berdasarkan hasil eksekusi `SATC-03`, dari 12 rekaman mentah yang dimasukkan ke basis data, berapa banyak baris rekaman yang disimpan di tabel rollup agregasi? Hitung rasio kompresi data yang diperoleh.
