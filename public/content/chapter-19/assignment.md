# Tugas & Rubrik — Chapter 19: Subsistem Telemetri Tahan Gangguan & Replay

## Skenario Tugas

Sebuah armada beranggotakan `100` sensor kualitas udara kampus melaporkan suhu, kelembapan, dan PM2.5 tiap `20 detik` ke satu broker MQTT lokal. Jaringan Wi-Fi kampus rutin melakukan *restart access point* pada malam hari selama ~10 menit.

## Instruksi Pengerjaan

1. **Perancangan Ring Buffer & Perhitungan Memori**:
   - Tentukan struktur `TelemetryRecord` ringkas (wajib memuat `seqId`, `timestamp`, `timeSynced`, serta nilai sensor) beserta ukuran memorinya (byte).
   - Hitung kapasitas slot minimum yang mampu menampung *outage* 20 menit (`dropped_oldest = 0`), serta jelaskan kebijakan ketika gangguan melampaui kapasitas tersebut (RAM vs persisten LittleFS saat listrik padam).
2. **Strategi SNTP & Backoff Anti-Thundering Herd**:
   - Uraikan prosedur `configTime()` UTC, deteksi waktu valid (`time_synced`), serta kurva *Exponential Backoff + Full Jitter* ($T_0$, $T_{\max}$, dan sumber keacakan `esp_random()`).
3. **Implementasi & Simulasi Ujung-ke-Ujung**:
   - Kembangkan variasi [`offline_buffer_sync.py`](content/chapter-19/src/offline_buffer_sync.py) atau [`offline_queue_ntp.ino`](content/chapter-19/src/offline_queue_ntp/offline_queue_ntp.ino) yang menyimulasikan:
     - Fase *online* $\rightarrow$ *outage* (antrean terisi) $\rightarrow$ *reconnect jitter* $\rightarrow$ *batch drain* bertahap + simulasi *lost ACK* dengan deduplikasi `(device_id, seq_id)`.
4. **Checklist Uji Kegagalan & Laporan Bukti**:
   - Cantumkan metrik uji aktual (*jumlah sampel produksi, kapasitas buffer, `dropped_oldest`, `duplicates_ignored`, `server_stored`*) dan nyatakan status verifikasi secara jujur.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Poin | Indikator Keberhasilan |
| --- | :---: | --- |
| Desain Ring Buffer & manajemen memori | 25 | *Struct* tetap bebas *heap fragmentation*, hitungan slot vs durasi *outage* tepat, kebijakan *Drop-Oldest* jelas. |
| Sinkronisasi waktu SNTP & strategi Jitter Backoff | 25 | Pemakaian UTC + flag `time_synced` akurat; *Full Jitter* mencegah *thundering herd* tanpa seed statis. |
| Implementasi replay & idempotent deduplication | 30 | `MAX_DRAIN_PER_TICK` non-blocking; `head` hanya maju saat ACK sukses; uji *lost ACK* tidak menggandakan data. |
| Kelengkapan log pengujian & kejujuran bukti | 20 | Output simulasi lengkap, memisahkan bukti software vs compile/hardware secara jujur. |
| **Total** | **100** | |

