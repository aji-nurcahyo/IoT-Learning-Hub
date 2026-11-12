# Chapter 19 — Connectivity Reliability, Time Synchronization & Offline Buffering

Di laboratorium, Wi-Fi dan broker MQTT tampak selalu aktif. Di lapangan—entah kebun percobaan, ruang pompa bawah tanah, atau gedung dengan *access point* padat—tautan nirkabel pasti mengalami *dropout*, pergantian *DHCP lease*, atau pemeliharaan server. Sistem IoT yang menganggap jaringan selalu online akan kehilangan data sensor tepat pada saat gangguan terjadi, atau bahkan membeku akibat pemanggilan blokir berulang. Bab ini merancang arsitektur perangkat tangguh dengan **sinkronisasi waktu SNTP**, **Circular Ring Buffer** statis bebas fragmentasi memori, **Exponential Backoff dengan Full Jitter**, serta **Idempotent Replay**.

![Arsitektur SNTP Time Sync, Ring Buffer Offline, dan Idempotent Replay](content/chapter-19/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, Anda diharapkan mampu:

1. Menjelaskan mengapa *timestamp* akurat (**UTC Epoch via SNTP**) esensial untuk telemetri terdistribusi serta cara menandai data secara jujur (`time_synced: false`) saat waktu belum tersinkronisasi.
2. Merancang **Circular Ring Buffer** berkapasitas tetap (*Fixed-Size Struct Array*) dengan kebijakan luapan **Drop-Oldest** tanpa kebocoran atau fragmentasi *heap*.
3. Menghitung dan menerapkan **Exponential Backoff dengan Full Jitter** untuk mencegah fenomena **Thundering Herd** saat ratusan perangkat pulih serentak.
4. Menerapkan mekanisme **Idempotent Ingest** berbasis pasangan kunci `(device_id, seq_id)` di sisi penerima agar pengiriman ulang (*retry* / QoS 1 / *replay*) tidak menciptakan baris data duplikat.
5. Mengimplementasikan *batch draining* non-blocking di ESP32 agar pengurasan antrean panjang tidak memicu reset *Watchdog Timer* (WDT).

## Prasyarat

- Pemahaman FSM koneksi Wi-Fi & *backoff* dasar ([Chapter 12](chapter-12)).
- Pemahaman *session persistence*, QoS 1/2, dan deduplikasi pesan pada MQTT ([Chapter 15](chapter-15)).

## Konsep dan teori

### 1. Sinkronisasi Waktu SNTP & Kejujuran Timestamp

Pada sistem *offline buffering*, sebuah bacaan sensor pada pukul `10:05` mungkin baru berhasil dikirim ke broker pukul `10:42` setelah Wi-Fi pulih. Jika *server* memberi *timestamp* saat pesan tiba (`server_received_at`), seluruh data selama `37 menit` gangguan akan menumpuk seolah terjadi bersamaan di pukul `10:42`—merusak grafik dan analisis tren!

Solusinya, perangkat wajib mencap waktu di **sisi tepi (edge)** memakai **UTC Unix Epoch** melalui protokol **SNTP** (*Simple Network Time Protocol*, port UDP `123`). Pada Arduino ESP32:

```cpp
configTime(0, 0, "pool.ntp.org", "time.google.com"); // Selalu UTC (offset 0) untuk payload JSON/CSV
```

Dua aturan penting waktu pada perangkat embedded:
1. **Simpan dan kirim selalu dalam UTC**; konversi ke zona waktu lokal (misalnya `WIB / UTC+7`) cukup dilakukan di *dashboard* atau lapisan presentasi.
2. **Jangan pernah memalsukan waktu sebelum SNTP siap**: setelah *cold boot*, jam internal ESP32 mulai dari `1970-01-01` (`epoch = 0`). Sebelum validasi (`epoch >= 1704067200`), catat nilai `millis()` bersama bendera eksplisit `"time_synced": false` agar *backend* tahu bahwa stempel waktu masih berupa *uptime* relatif.

### 2. Circular Ring Buffer & Manajemen Memori Embedded

Selama jaringan putus, sampel baru tetap diproduksi pada interval reguler. Menyimpannya memakai `std::vector` atau objek `String` yang terus bertambah secara dinamis di ESP32 akan cepat menghabiskan SRAM dan memicu *heap fragmentation* hingga *kernel panic*.

Pendekatan yang aman adalah **Circular Ring Buffer** berkapasitas tetap $N$ slot menggunakan *struct* berukuran seragam:

- Penunjuk **`head`** menunjuk elemen paling tua yang menunggu dikirim (dan **hanya dimajukan setelah ACK/publish berhasil**).
- Penunjuk **`tail`** menunjuk slot kosong berikutnya untuk data baru.
- Apabila antrean penuh (`count == N`), kebijakan **Drop-Oldest** menggeser `head` maju satu langkah untuk memberi ruang bagi data terbaru yang lebih relevan bagi pemantauan terkini, sambil menaikkan penghitung diagnostik `dropped_oldest`.
- **Batasan RAM vs Flash**: *Ring buffer* di SRAM bertahan saat Wi-Fi putus, tetapi akan hilang bila daya listrik mati total. Untuk ketahanan lintas pemadaman (*power loss*), persistenkan antrean ke **LittleFS** atau media eksternal (FRAM/microSD) dengan mempertimbangkan batas siklus tulis (*wear leveling*) memori flash.

### 3. Exponential Backoff dengan Full Jitter (Anti-Thundering Herd)

Bayangkan `500` node IoT di satu kawasan kampus kehilangan konektivitas bersamaan karena pemadaman router pusat selama 2 menit. Jika seluruh node memakai *backoff* deterministik ($T = \min(T_{\max}, T_0 \cdot 2^k)$), semua `500` node akan mencoba menyambung ulang pada detik ke-2, ke-4, ke-8, dan ke-16 **secara serentak**, menghantam *access point* dan broker MQTT (*Thundering Herd Problem*).

Dengan menambahkan **Full Jitter** (rekomendasi *AWS Architecture Blog* untuk *backoff* terdistribusi):

$$T_{\text{wait}}(k) = \text{Uniform}\left(0,\; \min(T_{\max},\; T_0 \cdot 2^k)\right)$$

Setiap perangkat memilih waktu tunggu acak seragam di rentang `[0, upper]`, menyebarkan beban koneksi ulang secara merata.

### 4. Idempotent Replay & Batch Draining Non-Blocking

Saat menguras antrean (*replay*) setelah pulih:
1. **Jangan menguras seluruh buffer dalam satu iterasi blokir**: jika terdapat `200` data tertunda dan Anda mengirim semuanya dalam satu loop `while` tanpa jeda/batas, tugas latar belakang FreeRTOS atau *Task Watchdog Timer* (WDT) dapat mengira `loop()` macet. Batasi pengurasan maksimal `K` item per siklus (misal `MAX_DRAIN_PER_TICK = 4`) atau beri `yield()` secara teratur.
2. **Idempotensi Ujung-ke-Ujung**: Jika pengiriman QoS 1 atau HTTP `POST` sudah diterima server tetapi paket `PUBACK`/`200 OK` hilang di tengah jalan, perangkat menganggap pengiriman gagal dan membiarkan item tetap di `head` untuk dikirim ulang nanti. Tanpa mekanisme deduplikasi di server berdasarkan kunci unik `(device_id, seq_id)`, data akan tercatat ganda. Server *ingest* idempoten mengecek apakah `(device_id, seq_id)` sudah pernah tersimpan: jika ya, abaikan penyimpanan ulang (*duplicate ignored*) namun tetap kembalikan `ACK` agar `head` perangkat bisa maju.

### 5. Worked Example — Simulasi `offline_buffer_sync.py`

Skrip [`offline_buffer_sync.py`](content/chapter-19/src/offline_buffer_sync.py) menjalankan skenario uji terkendali dengan hasil aktual:

1. **Uji Anti-Thundering Herd (50 Node, Percobaan ke-3)**:
   - Tanpa *jitter*: seluruh 50 node menjadwalkan koneksi ulang pada titik tunggal **`16.0 s`** (`unique_delays = 1`).
   - Dengan *Full Jitter*: terbentuk **`50` waktu tunda unik** tersebar antara **`0.40 s`** hingga **`15.99 s`**.
2. **Uji Ring Buffer Kapasitas `4` Slot Selama Outage `6` Sampel (`seq 3..8`)**:
   - Sampel `seq 1..2` dikirim langsung (`STORED_ACK`).
   - Saat *offline*, `seq 3..8` masuk ke *ring* berkapasitas 4 $\rightarrow$ 2 sampel paling tua (`seq 3, 4`) tergeser oleh kebijakan *Drop-Oldest* (`buffered = 4`, `dropped_oldest = 2`).
3. **Uji Idempotent Replay**:
   - Saat pulih, `seq 5` dikirim dua kali (menyimulasikan `PUBACK` yang hilang pada percobaan pertama). Percobaan ke-1 menghasilkan `STORED_ACK`, percobaan ke-2 mengembalikan **`DUPLICATE_ACK`** tanpa menduplikasi data di basis data server (`duplicates_ignored = 1`, total tersimpan bersih `7` sampel: `seq 1, 2, 5, 6, 7, 8, 9`).

## Latihan

Latihan konseptual, perhitungan *ring buffer* & *backoff*, serta modifikasi kode ESP32 tersedia pada tab **[Exercises](chapter-19#exercises)**.

## Tugas

Rancang dan simulasikan subsistem ketahanan konektivitas (*SNTP + Ring Buffer + Jittered Backoff + Idempotent Ingest*) untuk skenario pemadaman jaringan 30 menit pada tab **[Tugas & Rubrik](chapter-19#assignment)** (total bobot 100 poin).

## Ringkasan

- Berikan cap waktu di sisi perangkat memakai **UTC Epoch via SNTP**; saat belum tersinkronisasi, gunakan `uptime` dan tandai `"time_synced": false`.
- Gunakan **Circular Ring Buffer** statis (*fixed-size struct*) untuk menampung data saat *offline* tanpa risiko fragmentasi *heap*, dan kuras secara bertahap (`MAX_DRAIN_PER_TICK`) agar aman terhadap *Watchdog Timer*.
- Padukan **Exponential Backoff + Full Jitter** untuk mencegah *thundering herd* saat jaringan pulih, serta **Idempotent Key `(device_id, seq_id)`** di sisi penerima untuk menoleransi pengiriman ulang tanpa duplikasi.

## Referensi

1. Marc Brooker, *Exponential Backoff And Jitter (AWS Architecture Blog)*, [https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/).
2. Espressif Systems, *ESP-IDF Programming Guide: System Time & SNTP*, [https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/system_time.html](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/system_time.html).
3. IETF RFC 5905 / RFC 4330, *Simple Network Time Protocol (SNTP) & NTPv4*, [https://datatracker.ietf.org/doc/html/rfc5905](https://datatracker.ietf.org/doc/html/rfc5905).

