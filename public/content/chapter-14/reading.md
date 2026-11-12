# Chapter 14 — MQTT Fundamentals & Publish/Subscribe

## Overview

Pada skenario ratusan node sensor IoT yang mengirim *telemetry* berkala sekaligus menerima perintah kendali secara instan (*downlink*), arsitektur *Request–Response* seperti HTTP memiliki keterbatasan besar: server tidak dapat langsung mendorong perintah ke perangkat tanpa perangkat melakukan *polling* terus-menerus, dan *header* teks HTTP terlalu gemuk untuk pesan singkat.

**MQTT (Message Queuing Telemetry Transport)** adalah protokol standar OASIS berbasis pola **Publish/Subscribe** di atas TCP/IP yang sangat ringan (*header* tetap minimum hanya **2 byte**). Chapter ini membahas arsitektur *Publisher–Broker–Subscriber*, perancangan hierarki *topic*, aturan *wildcard* (`+` dan `#`), desain *payload* JSON, konfigurasi *Eclipse Mosquitto* lokal yang aman, serta implementasi klien MQTT non-blocking pada ESP32 (`PubSubClient`).

## Prasyarat

- Memahami TCP/IP, ports (`1883`/`8883`), dan sockets dari [Chapter 11](#/chapter/11).
- Menguasai koneksi Wi-Fi non-blocking & penyimpanan NVS dari [Chapter 12](#/chapter/12).
- Memahami perbandingan HTTP/REST vs pub/sub dan format JSON dari [Chapter 13](#/chapter/13).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Memetakan** arsitektur **Publish/Subscribe** (*Publisher*, *Broker*, *Subscriber*) dan membandingkan keunggulannya terhadap model *client–server* HTTP pada sistem IoT terdistribusi.
2. **Merancang** hierarki **MQTT Topic** yang terstruktur, konsisten, dan aman terhadap aturan *single-level wildcard* (`+`) serta *multi-level wildcard* (`#`).
3. **Menyusun** desain *payload* JSON dan mengonfigurasi **Eclipse Mosquitto** lokal dengan batas keamanan jaringan (*loopback* vs LAN + autentikasi).
4. **Mengimplementasikan** klien MQTT non-blocking pada ESP32 (`PubSubClient`) yang dapat mengirim *telemetry* dan menerima perintah aktuator melalui *callback*.

## Konsep dan teori

### 1. Arsitektur Publish/Subscribe & Decoupling

Pada MQTT, pengirim (*Publisher*) dan penerima (*Subscriber*) **tidak pernah terhubung langsung** dan tidak saling mengetahui alamat IP masing-masing. Keduanya hanya terhubung melalui koneksi TCP ke satu titik pusat yaitu **MQTT Broker**.

Tiga jenis pemisahan (*decoupling*) yang dihasilkan:
- **Space Decoupling**: Publisher tidak perlu tahu berapa banyak atau di mana lokasi IP para Subscriber.
- **Time Decoupling**: Dengan fitur sesi persisten & *retained messages* (dibahas di Chapter 15), penerbit dan pelanggan tidak harus selalu aktif di detik yang persis sama.
- **Synchronization Decoupling**: Pengiriman dan penerimaan berjalan asinkron melalui *callback* tanpa memblokir eksekusi sensor.

![Arsitektur MQTT Publish Subscribe, hierarki topic, dan aturan wildcard](content/chapter-14/diagram.svg)

### 2. Topic Hierarchy & Aturan Wildcard (`+` dan `#`)

**Topic** di MQTT adalah string UTF-8 yang dipisah oleh garis miring `/` (bersifat *case-sensitive*): `Temp` berbeda dengan `temp`!

**Pedoman Desain Topic yang Baik**:
- Gunakan pola hierarki konsisten: `<organisasi>/<lokasi>/<perangkat>/<kategori>` (misal `lab/gh01/node-01/telemetry` dan `lab/gh01/node-01/cmd/led`).
- **Jangan awali topic dengan `/`** (seperti `/lab/gh01`) karena menambah satu level string kosong di awal.
- **Jangan gunakan spasi** dan hindari simbol khusus di nama topic.

**Dua Wildcard untuk Subscribe** *(Publisher DILARANG mengirim ke topic yang mengandung `+` atau `#`!)*:
1. **Single-Level Wildcard (`+`)**: Mewakili tepat **satu** tingkat folder.
   - `lab/+/node-01/telemetry` cocok dengan `lab/gh01/node-01/telemetry`, tetapi **tidak cocok** dengan `lab/gh01/zona1/node-01/telemetry`.
2. **Multi-Level Wildcard (`#`)**: Mewakili **nol atau lebih** tingkat lanjutan dan **harus diletakkan sebagai karakter paling akhir setelah `/`**.
   - `lab/gh01/#` valid dan menangkap seluruh sub-topic di bawah `gh01`.
   - `lab/#/telemetry` **TIDAK VALID** secara protokol!
   - Menghindari `subscribe("#")` pada produksi publik/besar karena membanjiri klien dengan jutaan pesan sistem (`$SYS/...`).

### 3. Desain Payload MQTT yang Bersih

Karena MQTT bersifat *payload-agnostic* (mengirim *byte array* apa saja), disarankan menyepakati skema JSON ringkas dengan identitas node, *sequence number*, satuan eksplisit pada nama kunci, dan tanda sumber bila data sintetis:

```json
{"device_id":"esp32-gh01-node01","seq":1,"temp_c":28.75,"source":"synthetic"}
```

*(Catatan ukuran buffer: pada pustaka `PubSubClient`, ukuran buffer paket bawaan adalah `256 byte`! Jika payload JSON atau panjang topic melebihi batas tersebut, pesan akan gagal dikirim diam-diam kecuali Anda memanggil `mqtt.setBufferSize(512)`).*

### 4. Konfigurasi Eclipse Mosquitto Lokal yang Aman

**Eclipse Mosquitto** adalah broker MQTT ringan sumber terbuka (*open-source*).
- **Untuk uji satu komputer saja (loopback)**: gunakan `listener 1883 127.0.0.1` + `allow_anonymous true`.
- **Untuk perangkat ESP32 di LAN yang sama**: perangkat fisik tidak dapat menjangkau `127.0.0.1` PC! Anda perlu `listener 1883` pada antarmuka LAN, **aktifkan file password (`mosquitto_passwd` + `allow_anonymous false`)**, dan atur **ACL topic** agar node hanya boleh menulis ke topic-nya sendiri. Jangan pernah membuka broker tanpa autentikasi ke internet publik!

### 5. Implementasi Klien ESP32 (`PubSubClient`) & Uji Loopback (`mqtt_broker_sim.py`)

Pada [`mqtt_pubsub_client.ino`](content/chapter-14/src/mqtt_pubsub_client/mqtt_pubsub_client.ino):
- `mqtt.setServer(cfgBroker, 1883)` dan `mqtt.setCallback(onMqttMessage)` dikonfigurasi di `setup()`.
- Di dalam `loop()`, pemanggilan **`mqtt.loop()`** wajib berjalan rutin agar klien memproses paket masuk dan menjaga *keepalive ping* ke Broker tanpa memakai `delay()`.
- Untuk verifikasi protokol tanpa bergantung pada broker eksternal, skrip [`mqtt_broker_sim.py`](content/chapter-14/src/mqtt_broker_sim.py) mengimplementasikan paket biner asli MQTT 3.1.1 (`CONNECT` $\rightarrow$ `CONNACK`, `SUBSCRIBE` $\rightarrow$ `SUBACK`, `PUBLISH`) di soket TCP `127.0.0.1` serta menguji fungsi `topic_matches()` (`outputs.md`: seluruh pengujian *wildcard* dan transmisi loopback **PASS**). Firmware `.ino` masih berstatus **Belum diuji** terhadap compiler/broker nyata.

### 6. Common Mistakes & Troubleshooting

| Gejala Masalah | Penyebab Umum | Solusi |
| --- | --- | --- |
| `mqtt.connect()` gagal (`rc=-2` *Connect Failed*) | Broker mati, firewall memblokir TCP `1883`, atau salah pakai IP `127.0.0.1` | Pastikan Mosquitto berjalan pada IP LAN dan port `1883` diizinkan firewall |
| `mqtt.publish()` mengembalikan `false` untuk JSON panjang | Panjang `topic + payload + header` melebihi default `256 byte` `PubSubClient` | Panggil `mqtt.setBufferSize(512)` di `setup()` |
| Klien terus putus-sambung (*rc=5 / kick loop*) | **Dua perangkat memakai `clientId` yang sama!** | Buat `clientId` unik per perangkat (misal berbasis MAC address `WiFi.macAddress()`) |
| Pesan perintah tidak pernah memicu callback | Lupa memanggil `mqtt.loop()` secara rutin atau `delay()` memblokir `loop()` | Pastikan `mqtt.loop()` terpanggil di setiap iterasi `loop()` non-blocking |

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-14/exercises.md)):
1. Evaluasi pencocokan *wildcard* `+` dan `#` terhadap daftar topic nyata.
2. Diagnosis kasus *clientId* duplikat dan kegagalan `publish()` akibat ukuran buffer `PubSubClient`.
3. Menjalankan [`mqtt_broker_sim.py`](content/chapter-14/src/mqtt_broker_sim.py) dan memperluas skrip uji untuk memverifikasi beberapa subscriber dengan filter berbeda.

## Tugas

Rancang **Arsitektur Topic Hierarchy MQTT, Skema Payload & Implementasi Pub/Sub Lokal** untuk skenario *Smart Campus Monitoring* (detail & rubrik 100 poin di tab **Tugas & Rubrik** — [assignment.md](content/chapter-14/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Desain hierarki topic & aturan wildcard | 25 | Konsisten, tanpa leading `/`, bebas wildcard terbalik, penggunaan `+` dan `#` tepat |
| Desain skema payload JSON & keamanan broker | 25 | Payload ringkas berunit eksplisit, konfigurasi Mosquitto aman (tanpa anonymous publik) |
| Implementasi klien Pub/Sub non-blocking | 30 | `clientId` unik, `mqtt.loop()`, buffer cukup, penanganan callback perintah dan publish aman |
| Pengujian loopback/broker & kejujuran bukti | 20 | Uji transmisi pub-sub terdokumentasi dengan log asli dan status verifikasi jujur |

## Ringkasan

- MQTT menggunakan arsitektur **Publish/Subscribe** terpusat pada **Broker** untuk memisahkan pengirim dan penerima dalam ruang, waktu, dan sinkronisasi.
- Gunakan hierarki *topic* yang teratur (`lab/gh01/node-01/telemetry`), pahami batas wildcard (`+` = 1 level, `#` = multi-level di akhir), dan pastikan `clientId` selalu unik per node.
- Panggil `mqtt.loop()` secara non-blocking dan sesuaikan `setBufferSize()` bila payload melebihi 256 byte.
- Uji protokol biner MQTT 3.1.1 dan wildcard telah dieksekusi nyata via `mqtt_broker_sim.py` (`outputs.md`); kompilasi `.ino` menunggu instalasi core ESP32 selesai.

## Referensi

1. OASIS Standard, *MQTT Version 3.1.1 & 5.0 Specifications*, [https://mqtt.org/mqtt-specification/](https://mqtt.org/mqtt-specification/) (diperiksa 2026-11-11).
2. Eclipse Foundation, *Eclipse Mosquitto Documentation*, [https://mosquitto.org/documentation/](https://mosquitto.org/documentation/) (diperiksa 2026-11-11).
3. Nick O'Leary, *PubSubClient Arduino MQTT Library API*, [https://pubsubclient.knolleary.net/api](https://pubsubclient.knolleary.net/api) (diperiksa 2026-11-11).

