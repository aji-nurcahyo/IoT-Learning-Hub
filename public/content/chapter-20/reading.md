# Chapter 20 — Connected Device Capstone

Setelah menguasai fondasi jaringan TCP/IP, Wi-Fi *state machine*, REST/JSON, MQTT Pub/Sub beserta QoS/Retained/LWT, bus serial (*UART/I2C/SPI*), BLE, LPWAN, serta keandalan sinkronisasi waktu dan *offline buffering*, kita kini menyatukan seluruh komponen tersebut menjadi satu **Connected Environmental Monitoring System** ujung-ke-ujung. Proyek puncak Level 2 ini dirancang dengan pendekatan **Simulator-First + Broker Lokal** sehingga seluruh skenario—mulai dari *provisioning*, *live telemetry*, gangguan jaringan, kontrol lokal *fail-safe*, hingga pengujian *Last Will*—dapat diuji secara menyeluruh tanpa bergantung pada layanan cloud berbayar.

![Arsitektur Capstone Level 2: ESP32 Connected Environmental Monitoring System](content/chapter-20/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan capstone ini, Anda diharapkan mampu:

1. Mengintegrasikan **NVS (`Preferences`)**, **HTTP Client**, **SNTP**, **Offline Ring Buffer**, dan **MQTT (`PubSubClient`)** ke dalam arsitektur firmware non-blocking yang bersih dan modular.
2. Menjamin fungsi kontrol kritis lokal (*histeresis kipas/relay*) tetap bekerja secara mandiri meskipun Wi-Fi atau broker MQTT terputus (*local fail-safe*).
3. Menerapkan pemulihan konektivitas otomatis menggunakan **Full-Jitter Exponential Backoff** serta pengurasan antrean bertahap (*batch drain*) tanpa memicu reset *Watchdog Timer*.
4. Menghubungkan perangkat ke **HTTP config endpoint lokal** dan **broker MQTT lokal** lengkap dengan payload JSON berstempel UTC, *Retained Status*, **LWT `"offline"`**, serta topik perintah jarak jauh (`cmd`).
5. Menyusun dan mengeksekusi **6 kasus uji penerimaan** (*connectivity & fault-injection test cases*) secara objektif serta mendokumentasikan bukti hasil uji secara jujur.

## Prasyarat

- Menyelesaikan seluruh materi dan latihan **Chapter 11–19** (khususnya [Chapter 12](chapter-12), [Chapter 13](chapter-13), [Chapter 14](chapter-14), [Chapter 15](chapter-15), dan [Chapter 19](chapter-19)).
- Memahami dasar pembacaan ADC1 ESP32 dan kontrol histeresis aktuator ([Chapter 07](chapter-07) dan [Chapter 09](chapter-09)).

## Konsep dan teori

### 1. Spesifikasi Arsitektur End-to-End

Sistem *Connected Environmental Monitoring* terdiri atas tiga subsistem yang terhubung melalui jaringan IP lokal (LAN / Wi-Fi):

1. **Perangkat Lapangan (`node-01`)**: Sensor suhu analog pada `GPIO34` (*ADC1_CH6*, aman dipakai bersamaan dengan Wi-Fi aktif, tidak seperti ADC2), indikator koneksi pada `GPIO2`, aktuator kipas/relay pada `GPIO26`, dan tombol lokal `GPIO27` (terhubung ke [`wokwi_diagram.json`](content/chapter-20/src/wokwi_diagram.json)).
2. **Firmware ESP32 ([`connected_env_capstone.ino`](content/chapter-20/src/connected_env_capstone/connected_env_capstone.ino) & [`config.h`](content/chapter-20/src/connected_env_capstone/config.h))**:
   - **Lapisan Konfigurasi**: Memuat `ssid`, `brokerHost`, `sampleMs`, `tempHighC`, dan `tempHystC` dari NVS (`Preferences` namespace `"capstone"`). Bila *HTTP config server* tidak terjangkau saat boot, perangkat otomatis jatuh kembali (*fallback*) ke nilai NVS sehingga tetap beroperasi.
   - **Lapisan Kontrol Lokal (*Fail-Safe*)**: Membandingkan suhu terhadap ambang `tempHighC` dengan pita histeresis `tempHystC` ($1{,}5\,^\circ\text{C}$) **sebelum** memeriksa status Wi-Fi—memastikan pendinginan tetap menyala walaupun jaringan mati berjam-jam.
   - **Lapisan Buffering & Time Sync**: Memakai `configTime(0, 0, ...)` (UTC) dengan pengecekan `time_synced`, lalu memasukkan `TelemetryFrame` berukuran tetap ke *Circular Ring Buffer* `32` slot (*Drop-Oldest*).
   - **Lapisan Konektivitas**: Mengelola *reconnect* Wi-Fi dan MQTT secara terpisah memakai `computeFullJitterMs()` (`esp_random()`), menarik pembaruan konfigurasi lewat `HTTP GET`, mengirim JSON ke `iot/lab/node-01/telemetry`, mendaftarkan **LWT** `"offline"` (*QoS 1, Retained*) pada `iot/lab/node-01/status`, mempublikasikan `"online"` (*Retained*) saat terhubung, serta berlangganan `iot/lab/node-01/cmd`.
3. **Layanan Lokal (Tanpa Cloud Berbayar)**: Server HTTP ringan (`GET /api/v1/config/node-01`) dan broker MQTT lokal (seperti **Eclipse Mosquitto** pada LAN atau broker loopback Python untuk uji otomatis) ditambah *subscriber* dengan indeks idempotensi `(dev, seq)`.

### 2. Kontrak Payload JSON & Topik MQTT

| Topik | Arah | Retained / LWT | Format Payload & Fungsi |
| :--- | :---: | :---: | :--- |
| `iot/lab/node-01/status` | Node $\rightarrow$ Broker | **Retained + LWT** | `"online"` saat *connected*, `"offline"` otomatis oleh broker saat koneksi TCP terputus mendadak |
| `iot/lab/node-01/telemetry` | Node $\rightarrow$ Broker | Non-retained | `{"dev":"node-01","seq":1,"ts":1762822800,"synced":true,"temp":27.80,"th":30.00,"relay":false,"q":0,"drop":0}` |
| `iot/lab/node-01/cmd` | Controller $\rightarrow$ Node | Non-retained | `{"cmd":"set_threshold","temp_high_c":29.0}` (divalidasi rentang `15..60 C` lalu disimpan ke NVS) |

Perhatikan bahwa panjang string JSON di atas berkisar $\sim 105\text{–}120\text{ byte}$, jauh di dalam batas `mqtt.setBufferSize(512)` serta buffer stack `char json[220]` tanpa satu pun objek `String` dinamis di jalur pengiriman telemetri.

### 3. Alur State Machine & Pencegahan Error Kritis

Beberapa keputusan rekayasa di dalam [`connected_env_capstone.ino`](content/chapter-20/src/connected_env_capstone/connected_env_capstone.ino) secara langsung menjawab sumber bug tersering di proyek IoT:

1. **Pengecekan Waktu Rollover-Safe**: Semua timer memakai `static_cast<long>(nowMs - targetMs) >= 0` agar bebas masalah *overflow* `millis()` 32-bit.
2. **Pemisahan `loop()` Menjadi 5 Tahap**: Akuisisi + kontrol lokal $\rightarrow$ penjaga Wi-Fi $\rightarrow$ sinkronisasi HTTP sekali per sesi $\rightarrow$ penjaga + `mqtt.loop()` $\rightarrow$ *batch drain* maksimal `4` item per putaran (`CAPSTONE_MAX_DRAIN_PER_TICK = 4`).
3. **Validasi Perintah Eksternal (*Input Sanitization*)**: Perintah `temp_high_c` lewat `iot/lab/node-01/cmd` hanya diterima bila berada di rentang aman `15.0..60.0 C`; perintah berbahaya (`-99 C` atau `999 C`) ditolak sebelum merusak aktuator atau menulis ulang NVS.

### 4. Worked Example — Uji Penerimaan 6 Kasus (`capstone_connectivity_test.py`)

Skrip [`capstone_connectivity_test.py`](content/chapter-20/src/capstone_connectivity_test.py) menjalankan **HTTP Server lokal** dan **Broker MQTT 3.1.1 TCP lokal** pada `127.0.0.1` lalu memverifikasi enam skenario secara otomatis (`outputs.md`):

1. **`TC-01` (HTTP Config)**: `GET /api/v1/config/node-01` mengembalikan `200 OK` dan ambang awal `temp_high_c=30.0 C`.
2. **`TC-02` (LWT + Retained Status)**: Node `node-01` mengirim `CONNECT` membawa *Last Will* `"offline"` (*Retained*), menyusul `PUBLISH` `"online"` (*Retained*); *monitor subscriber* langsung menerimanya.
3. **`TC-03` (Live JSON Telemetry)**: `seq=1..2` terkirim lengkap dengan `ts` UTC dan `synced=true`.
4. **`TC-04` (Outage Buffering + Local Fail-Safe)**: Selama link putus, `seq=3..6` tertampung rapi di *ring buffer* (`depth=4`) dan suhu `30.80 C >= 30.00 C` memicu `relay=true` secara lokal.
5. **`TC-05` (Replay + Idempotent Deduplication)**: Saat pulih, antrean dikuras dan percobaan kirim ulang `seq=3` (menyimulasikan *lost ACK*) ditolak duplikasinya (`stored=6 unique, duplicates_ignored=1`).
6. **`TC-06` (Remote Command + Ungraceful LWT)**: Perintah `{"cmd":"set_threshold","temp_high_c":29.0}` diterima node, kemudian penutupan soket mendadak tanpa paket `DISCONNECT` memicu broker menyiarkan LWT `"offline"` ke *monitor subscriber*.

### 5. Panduan Troubleshooting Capstone

- **Serial mencetak `MQTT Failed rc=-2` terus-menerus**: IP `brokerHost` di NVS tidak menunjuk mesin tempat Mosquitto/server berjalan, atau *Windows Firewall* memblokir TCP port `1883`.
- **Pesan JSON tidak muncul meski `mqtt.publish()` dipanggil**: Ukuran paket melebihi buffer bawaan `PubSubClient` (`256 B`) $\rightarrow$ pastikan memanggil `mqtt.setBufferSize(512)` pada `setup()`.
- **Perubahan `temp_high_c` hilang setelah reset**: Lupa memanggil `saveRuntimeThresholdsToNvs()` (`prefs.putFloat(...)`) setelah memproses perintah MQTT atau HTTP.

## Latihan

Latihan pengujian skema error, audit kontrak JSON/topik, serta latihan perluasan fitur tersedia pada tab **[Exercises](chapter-20#exercises)**.

## Tugas

Selesaikan rancangan dan verifikasi proyek **Connected Environmental Monitoring Capstone** pada tab **[Tugas & Rubrik](chapter-20#assignment)** (total bobot 100 poin).

## Ringkasan

- Sistem IoT yang layak produksi menggabungkan **kontrol lokal *fail-safe***, **penyimpanan konfigurasi persisten (NVS)**, **HTTP provisioning/fallback**, **MQTT dengan LWT & Retained status**, **cap waktu SNTP UTC**, serta **Offline Ring Buffer + Idempotent Replay**.
- Seluruh alur konektivitas dapat diuji terlebih dahulu memakai infrastruktur lokal (*loopback* HTTP + broker Mosquitto lokal / `capstone_connectivity_test.py`) sebelum diuji pada hardware fisik.
- Kejujuran pencatatan status verifikasi (`software`, `compile`, `simulator`, `hardware`) memisahkan mana fungsi yang telah terbukti nyata dan mana yang masih perlu diuji di papan fisik.

## Referensi

1. OASIS Standard, *MQTT Version 3.1.1 / 5.0 Specification*, [https://mqtt.org/mqtt-specification/](https://mqtt.org/mqtt-specification/).
2. Eclipse Foundation, *Eclipse Mosquitto Open Source MQTT Broker Documentation*, [https://mosquitto.org/documentation/](https://mosquitto.org/documentation/).
3. Espressif Systems, *Arduino-ESP32 Libraries (WiFi, HTTPClient, Preferences, SNTP)*, [https://docs.espressif.com/projects/arduino-esp32/en/latest/](https://docs.espressif.com/projects/arduino-esp32/en/latest/).

