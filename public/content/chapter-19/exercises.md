# Exercises — Chapter 19: Reliability, Time Sync & Offline Buffering

## A. Pertanyaan Konseptual

1. Mengapa pemakaian *timestamp* `server_received_at` saja tidak memadai untuk node IoT yang memiliki mekanisme *offline buffering*?
2. Mengapa *firmware* ESP32 harus menyimpan waktu telemetri dalam **UTC** dengan flag `time_synced`, dan mengapa panggilan `random(min, max)` untuk *backoff jitter* sebaiknya memakai `esp_random()` bukan `randomSeed(1234)`?
3. Jelaskan mengapa kombinasi *client retry* (`at-least-once`) dan *server deduplication* berbasis `(device_id, seq_id)` penting bahkan ketika protokol transport-nya sudah memakai TCP/MQTT.

## B. Analisis Kapasitas Buffer & Backoff (`offline_buffer_sync.py`)

4. Sebuah node mengambil sampel setiap **`15 detik`** saat router Wi-Fi padam selama **`45 menit`**:
   - a) Hitung total sampel yang dihasilkan selama gangguan.
   - b) Berapa kapasitas *ring buffer* minimum (dalam slot dan dalam byte jika 1 `struct TelemetryRecord` berukuran `24 byte`) agar **`dropped_oldest == 0`**?
   - c) Jika ukuran *ring buffer* dibatasi hanya `100` slot, berapa `dropped_oldest` dan rentang `seq_id` mana yang hilang bila gangguan dimulai di `seq = 50`?
5. Modifikasi [`offline_buffer_sync.py`](content/chapter-19/src/offline_buffer_sync.py) untuk menjalankan `capacity = 8` selama *outage* `10` sampel dan uji kasus **3 kali *lost ACK*** berturut-turut pada `seq` yang sama. Pastikan `server_stored` tidak bertambah ganda.

## C. Latihan Firmware ESP32 (`offline_queue_ntp.ino`)

6. Pada [`offline_queue_ntp.ino`](content/chapter-19/src/offline_queue_ntp/offline_queue_ntp.ino), penjadwalan ulang memakai kondisi `nowMs >= nextReconnectMs`. Jelaskan apakah ekspresi tersebut berisiko pada *rollover* `millis()` setelah ~49,7 hari, dan tulis ulang ekspresi perbandingannya memakai pola aman `static_cast<long>(nowMs - nextReconnectMs) >= 0`!
7. Tambahkan bidang diagnostik `uint32_t droppedOldest` pada output JSON di fungsi `mockTransportSend()` agar *backend* pemantau kesehatan armada mengetahui apabila antrean node pernah meluap.

## Expected Output Acuan

Menjalankan [`offline_buffer_sync.py`](content/chapter-19/src/offline_buffer_sync.py) tanpa modifikasi harus menghasilkan nilai persis seperti pada [`outputs.md`](content/chapter-19/outputs.md):

- `[JITTER] attempt=3, 50 nodes without jitter -> unique_delays=1 (all at 16.0 s!)`
- `[JITTER] attempt=3, 50 nodes full-jitter    -> unique_delays=50, min=0.40 s, max=15.99 s`
- `[OFFLINE] pushed 6 items into capacity=4 ring -> buffered=4, dropped_oldest=2`
- `[SUMMARY] server_stored=7, duplicates_ignored=1, ring_dropped_oldest=2`.

