# Source Code — Chapter 19: Connectivity Reliability, Time Synchronization & Offline Buffering

## Daftar Berkas

1. [`offline_buffer_sync.py`](src/offline_buffer_sync.py) — Simulasi *Circular Ring Buffer* (`FixedRingBuffer`) berkapasitas tetap dengan kebijakan *Drop-Oldest*, perbandingan *Exponential Backoff* tanpa *jitter* vs *Full Jitter* untuk 50 node sekaligus (anti-*thundering herd*), serta server ingest idempoten berdasarkan pasangan kunci `(device_id, seq_id)`.
2. [`offline_queue_ntp.ino`](src/offline_queue_ntp/offline_queue_ntp.ino) — Sketsa ESP32 yang menggabungkan:
   - Sinkronisasi waktu UTC via SNTP (`configTime(0, 0, "pool.ntp.org", "time.google.com")`) dan pengecekan epoch valid `>= 1704067200`
   - Penyimpanan sampel ke *struct ring buffer* statis (`RING_CAPACITY = 32`, nol alokasi `String` *heap* dinamis)
   - *Full-jitter exponential backoff* memakai RNG perangkat keras `esp_random()`
   - Pengurasan antrean bertahap (`MAX_DRAIN_PER_TICK = 4`) agar *watchdog timer* (WDT) tidak terpicu saat antrean penuh terkuras.
3. [`telemetry.csv`](telemetry.csv) — Contoh jejak data *online -> offline buffering -> replay -> live* dengan kolom `time_synced` dan `buffer_depth`.

## Cara Menjalankan

```bash
python public/content/chapter-19/src/offline_buffer_sync.py
```

Sketsa [`offline_queue_ntp.ino`](src/offline_queue_ntp/offline_queue_ntp.ino) dikompilasi untuk target `esp32:esp32:esp32` menggunakan Arduino CLI.

