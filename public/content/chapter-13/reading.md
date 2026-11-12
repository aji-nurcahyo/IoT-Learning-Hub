# Chapter 13 — HTTP, REST APIs & JSON

## Overview

Sebelum protokol *publish/subscribe* seperti MQTT populer di ranah sensor nirkabel, sebagian besar integrasi layanan web mengandalkan **HTTP (Hypertext Transfer Protocol)** dan arsitektur **REST (Representational State Transfer)** dengan format pertukaran data **JSON**. Sampai hari ini, HTTP/REST tetap krusial dalam IoT untuk *device provisioning*, mengunduh konfigurasi awal (*bootstrap config*), memperbarui *Firmware* OTA, serta mengirim *telemetry* ke API web standar atau *Edge Gateway*.

Chapter ini mengupas metode HTTP, anatomi *request/response*, makna *status code* untuk logika *retry* di *Firmware*, serialisasi JSON yang aman terhadap memori ESP32, implementasi `HTTPClient`, manajemen *timeout*, serta fondasi keamanan **TLS/HTTPS**.

## Prasyarat

- Memahami TCP/IP, port `80`/`443`, dan sockets dari [Chapter 11](#/chapter/11).
- Memahami manajemen koneksi Wi-Fi non-blocking dan penyimpanan NVS dari [Chapter 12](#/chapter/12).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Merancang** kontrak endpoint **REST API** (`GET`, `POST`, `PUT`, `DELETE`) dan skema payload **JSON** yang konsisten beserta satuan fisik eksplisit.
2. **Membedakan** kategori *HTTP Status Codes* (`2xx`, `4xx`, `5xx`, serta kode error transport negatif di ESP32) untuk menentukan kebijakan *retry* yang tepat.
3. **Mengimplementasikan** klien HTTP pada ESP32 (`HTTPClient`) dengan **timeout eksplisit**, pembersihan koneksi (`http.end()`), dan serialisasi JSON hemat *heap*.
4. **Menjelaskan** peran **TLS/HTTPS** (enkripsi, integritas, verifikasi sertifikat CA) serta risiko penggunaan `setInsecure()`.

## Konsep dan teori

### 1. Anatomi HTTP Request/Response & Metode REST

HTTP bekerja dengan pola **Request–Response** (*client-initiated* di atas TCP): klien membuka koneksi, mengirim permintaan, dan menunggu balasan server.

```http
POST /api/v1/telemetry HTTP/1.1
Host: 192.168.10.50:8000
Content-Type: application/json
X-Device-Id: esp32-node-01
Content-Length: 74

{"device_id":"esp32-node-01","seq":1,"temp_c":28.40,"source":"synthetic"}
```

Empat metode REST paling umum pada IoT:

| Metode | Fungsi REST | Contoh Endpoint IoT | Idempoten? |
| --- | --- | --- | --- |
| **`GET`** | Mengambil data / konfigurasi (*read-only*) | `GET /api/v1/devices/node-01/config` | Ya |
| **`POST`** | Membuat entri baru / mengirim *telemetry* baru | `POST /api/v1/telemetry` | Tidak (kecuali dicegah server via `seq`/kunci) |
| **`PUT`** | Memperbarui seluruh status *resource* tertentu | `PUT /api/v1/devices/node-01/shadow` | Ya |
| **`DELETE`** | Menghapus registrasi atau antrean | `DELETE /api/v1/devices/node-01` | Ya |

### 2. HTTP Status Codes & Kebijakan Retry Cerdas

![Anatomi HTTP Request Response REST JSON, kebijakan retry, dan TLS](content/chapter-13/diagram.svg)

Kesalahan umum di *Firmware* adalah melakukan *retry* tanpa membedakan penyebab error. Gunakan aturan berdasarkan kelompok kode status:

| Kode Status | Arti | Aksi yang Benar pada Firmware ESP32 |
| --- | --- | --- |
| `200 OK` / `201 Created` | Sukses diproses / data tersimpan | Hapus item dari *buffer* lokal, reset penghitung error |
| `400 Bad Request` | Format JSON rusak / field wajib kurang | **JANGAN retry!** Catat error & buang/karantina paket |
| `401 Unauthorized` / `403` | Token API salah atau kedaluwarsa | **JANGAN retry cepat!** Tandai butuh *re-provisioning* |
| `404 Not Found` | Path URL salah | **JANGAN retry!** Periksa konfigurasi endpoint |
| `429 Too Many Requests` | Melebihi *rate limit* server | Perpanjang interval kirim (*backoff*) |
| `500` / `503` (`5xx`) | Server gagal internal / sibuk sementara | **Retry terbatas** (misal maks 2–3x dengan jeda) |
| Kode `< 0` di `HTTPClient` | Timeout TCP, koneksi ditolak, DNS gagal | **Retry terbatas** atau tahan data di *offline buffer* |

### 3. Serialisasi & Parsing JSON yang Aman di MCU

**JSON** bersifat *human-readable* dan menjadi standar de facto REST API, namun memiliki dua tantangan di mikrokontroler:
1. **Ukuran teks lebih besar** dibanding format biner (misal `{"temp_c":28.40}` memakan 16 byte untuk satu angka `float`).
2. **Fragmentasi Heap**: Membangun JSON dengan operator `+` pada objek `String` Arduino berulang kali dapat memecah *SRAM heap*.

**Solusi untuk Serialisasi (Mengirim Data)**: Gunakan buffer karakter statis `char payload[160]` + `snprintf()`, seperti di [`http_rest_client.ino`](content/chapter-13/src/http_rest_client/http_rest_client.ino). Untuk **Deserialisasi (Parsing Response)** bersarang yang kompleks, gunakan pustaka seperti **ArduinoJson** dengan ukuran terukur (*JsonDocument*) serta selalu periksa nilai kembalian error parsing sebelum membaca field.

### 4. HTTP Client pada ESP32, Timeout & Pembersihan Koneksi

Pada pustaka bawaan `HTTPClient.h` di *Arduino-ESP32*:
- **Selalu atur `http.setTimeout(3000)`**: Tanpa batas waktu yang ketat, `HTTPClient` dapat menunggu hingga 5–15 detik saat server macet dan memblokir `loop()`.
- **Selalu panggil `http.end()`** setelah setiap transaksi (baik sukses maupun gagal) agar *socket* TCP dan buffer memori dikembalikan ke sistem *lwIP*.
- **Trade-off HTTP vs MQTT**: Karena setiap `POST` membawa ratusan byte *HTTP header* teks dan membuka/mengelola sesi *request-response*, HTTP sangat cocok untuk transaksi berkala (misal tiap 1–15 menit atau *config fetch*), sedangkan pengiriman frekuensi tinggi ($1\text{ Hz}$) dari ratusan node lebih efisien dengan MQTT (Chapter 14).

### 5. TLS/HTTPS Fundamentals pada ESP32

Mengirim token autentikasi atau data sensitif melalui HTTP polos (*plaintext* port `80`) berarti siapa pun di jalur jaringan yang sama dapat menyadap atau memodifikasi pesan. **HTTPS** membungkus HTTP di dalam terowongan **TLS (*Transport Layer Security*)** pada port `443`:
1. **Enkripsi**: Isi *header* (termasuk API Key) dan *body JSON* terenkripsi.
2. **Integritas**: Setiap modifikasi paket di tengah jalan terdeteksi.
3. **Otentikasi Server**: ESP32 memverifikasi sertifikat server menggunakan **Root CA Certificate** yang ditanam di *Firmware* (`WiFiClientSecure::setCACert(root_ca)`).

**Peringatan Keras**: Memanggil `client.setInsecure()` menonaktifkan verifikasi sertifikat CA sehingga rentan serangan *Man-in-the-Middle* (MITM). Selain itu, verifikasi masa berlaku sertifikat TLS membutuhkan waktu jam perangkat yang akurat (disinkronkan via **NTP** — dibahas di Chapter 19).

### 6. Worked Example & Pengujian Loopback (`http_rest_sim.py`)

Untuk membuktikan perilaku kontrak REST dan kebijakan *retry* tanpa bergantung pada layanan cloud berbayar, skrip [`http_rest_sim.py`](content/chapter-13/src/http_rest_sim.py) menjalankan server HTTP lokal nyata pada `127.0.0.1` dan mengeksekusi tiga skenario (hasil aktual di [`outputs.md`](content/chapter-13/outputs.md)):
1. **Transient `503` $\rightarrow$ Retry $\rightarrow$ `201 Created`**: Percobaan 1 menerima `503 Service Temporarily Unavailable`; klien melakukan *retry* dan sukses `201 {"accepted": True, "seq": 1}` pada percobaan 2.
2. **Payload tidak lengkap (`400 Bad Request`)**: Server menolak dengan `400 {"error": "missing_required_fields"}`; klien **langsung berhenti tanpa mengulang**.
3. **`GET /api/v1/devices/esp32-node-01/config`**: Server mengembalikan `200 OK` berisi JSON konfigurasi (`sample_ms: 5000`, `t_high_c: 30.0`).

### 7. Common Mistakes & Troubleshooting

| Gejala Error | Penyebab Umum | Solusi |
| --- | --- | --- |
| `HTTPClient` mengembalikan `-1` (`HTTPC_ERROR_CONNECTION_REFUSED`) | Server lokal mati, port salah, firewall memblokir, atau memakai `127.0.0.1` di kode ESP32 | Gunakan IP LAN server, pastikan server *bind* ke `0.0.0.0`, dan buka port di firewall |
| `HTTP 400` berulang kali | Header `Content-Type: application/json` lupa dipasang atau tanda kutip JSON cacat | Tambahkan `http.addHeader("Content-Type", "application/json")` dan validasi format JSON |
| Memori *heap* habis setelah puluhan permintaan | Lupa memanggil `http.end()` atau membuat objek `HTTPClient` tanpa menutup socket | Pastikan `http.end()` dipanggil di setiap jalur keluar fungsi |
| HTTPS gagal handshake di ESP32 | Jam sistem masih tahun 1970 (belum NTP) atau sertifikat Root CA salah | Sinkronkan waktu via NTP (`configTime`) dan perbarui PEM Root CA |

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-13/exercises.md)):
1. Memilih metode REST (`GET/POST/PUT/DELETE`) dan status code yang tepat untuk berbagai kasus API IoT.
2. Menghitung ukuran *header + body* HTTP/1.1 dibanding payload JSON mentah.
3. Menjalankan [`http_rest_sim.py`](content/chapter-13/src/http_rest_sim.py) dan memperluas handler server lokal untuk memvalidasi API Key (`401 Unauthorized`) serta endpoint `PUT`.

## Tugas

Rancang **Kontrak REST API Telemetry & Klien HTTP ESP32 Tahan Error** lengkap dengan server uji lokal Python (detail di tab **Tugas & Rubrik** — [assignment.md](content/chapter-13/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Desain kontrak REST API & skema JSON | 25 | Endpoint semantik (`GET/POST`), header tepat, skema JSON berunit eksplisit |
| Penanganan status code, timeout & retry | 30 | Membedakan `2xx`, `4xx` (tanpa retry), `5xx`/timeout (retry terbatas), serta `http.end()` |
| Implementasi client & server uji lokal | 25 | Kode Python server+client berjalan nyata atau firmware terstruktur tanpa secret hardcoded |
| Analisis TLS/HTTPS & kejujuran bukti | 20 | Pemahaman CA verification vs `setInsecure()` dan pelaporan log aktual yang jujur |

## Ringkasan

- REST API di atas HTTP menggunakan pola *Request–Response* dengan metode `GET`, `POST`, `PUT`, `DELETE` dan payload JSON berstruktur.
- Kebijakan *retry* pada klien ESP32 harus membedakan kesalahan *client* (`4xx` — jangan ulang) dari kegagalan sementara jaringan/server (`5xx` / kode `< 0` — ulang terbatas dengan jeda).
- Gunakan *timeout* eksplisit, buffer statis `snprintf()`, `http.end()`, dan verifikasi sertifikat CA (bukan `setInsecure()`) saat memakai HTTPS.
- Pengujian *loopback* HTTP nyata telah dijalankan via `http_rest_sim.py` (`outputs.md`); kompilasi `.ino` sedang menanti selesainya instalasi core ESP32.

## Referensi

1. IETF RFC 9110, *HTTP Semantics*, [https://datatracker.ietf.org/doc/html/rfc9110](https://datatracker.ietf.org/doc/html/rfc9110) (diperiksa 2026-11-11).
2. IETF RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format*, [https://datatracker.ietf.org/doc/html/rfc8259](https://datatracker.ietf.org/doc/html/rfc8259) (diperiksa 2026-11-11).
3. Espressif Systems, *ESP-IDF ESP HTTP Client & mbedTLS Guide*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/esp_http_client.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/esp_http_client.html) (diperiksa 2026-11-11).

