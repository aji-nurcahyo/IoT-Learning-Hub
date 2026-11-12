# Chapter 15 — MQTT QoS, Sessions, Retained Messages & Last Will

## Overview

Mengirim pesan ke Broker dengan `mqtt.publish()` tidak otomatis menjamin pesan tersebut sampai ke seluruh penerima, atau tidak selalu memberitahu dashboard bila perangkat di lapangan mendadak mati listrik. Protokol MQTT menyediakan mekanisme keandalan terukur berupa **Quality of Service (QoS 0, 1, 2)**, **Session Persistence (`cleanSession` / `Session Expiry`)**, **Retained Messages**, **Keepalive**, serta **Last Will and Testament (LWT)**.

Chapter ini membedah secara mendalam jaminan pengiriman masing-masing tingkat QoS beserta *trade-off* jumlah paketnya, penanganan duplikasi pesan pada QoS 1, perilaku sesi dan pola *reconnect* antara **MQTT 3.1.1 dan MQTT 5.0**, serta praktik implementasi LWT dan status *retained* pada ESP32.

## Prasyarat

- Menguasai arsitektur Publish/Subscribe, topic hierarchy, dan wildcard MQTT dari [Chapter 14](#/chapter/14).
- Memahami perbedaan transport TCP dan overhead paket dari [Chapter 11](#/chapter/11).

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Membandingkan** **QoS 0, QoS 1, dan QoS 2** berdasarkan mekanisme *handshake*, jumlah paket, jaminan pengiriman, dan beban memori.
2. **Merancang** mekanisme penanganan **duplikasi pesan (*idempotency*)** pada QoS 1 serta menjelaskan mengapa jaminan QoS bersifat *per-hop* (*Client–Broker*), bukan *end-to-end* langsung.
3. **Mengonfigurasi** **Retained Messages**, **Keepalive**, dan **Last Will and Testament (LWT)** untuk mendeteksi perangkat *offline* secara akurat.
4. **Membedakan** perilaku *Session* (`cleanSession` vs *Persistent Session*), pola *reconnect*, serta fitur baru **MQTT 5.0** dibandingkan **MQTT 3.1.1**.

## Konsep dan teori

### 1. Quality of Service (QoS 0, 1, 2) & Jaminan Per-Hop

MQTT mendefinisikan tiga tingkat QoS yang berlaku pada **masing-masing lompatan (*per-hop*)**—yakni antara Publisher $\leftrightarrow$ Broker dan antara Broker $\leftrightarrow$ Subscriber (QoS pengiriman ke Subscriber adalah nilai $\min(\text{QoS}_{\text{pub}}, \text{QoS}_{\text{sub}})$):

| Tingkat QoS | Nama Resmi | Alur Paket | Jaminan & Risiko | Cocok Untuk |
| --- | --- | --- | --- | --- |
| **QoS 0** | *At most once* | `PUBLISH` (1 paket) | Bisa hilang; **tidak pernah duplikat** | *Telemetry* suhu rutin tiap 5 s yang nilainya cepat tergantikan |
| **QoS 1** | *At least once* | `PUBLISH` $\rightarrow$ `PUBACK` (2 paket) | Pasti sampai (di-retry hingga `PUBACK` tiba); **bisa duplikat** (`DUP=1`) | Perintah kontrol, event alarm, *telemetry* penting + *dedup* |
| **QoS 2** | *Exactly once* | `PUBLISH` $\rightarrow$ `PUBREC` $\rightarrow$ `PUBREL` $\rightarrow$ `PUBCOMP` (4 paket) | Pasti sampai **tepat satu kali** (tanpa duplikat); paling lambat & berat | Transaksi billing / pencatatan kWh kritis yang tak boleh ganda |

![Aliran paket MQTT QoS 0/1/2, Retained Message, dan Last Will](content/chapter-15/diagram.svg)

### 2. Duplicate Handling & Idempotensi pada QoS 1

Pada QoS 1, apabila Broker sudah menerima `PUBLISH` lalu mengirim `PUBACK`, namun `PUBACK` tersebut hilang di jaringan Wi-Fi, Publisher akan mengira pesan belum sampai dan mengirim ulang `PUBLISH` dengan flag **`DUP=1`**. Akibatnya, **Subscriber bisa menerima pesan yang sama dua kali!**

**Solusi Rekayasa**:
- Selalu sertakan `seq` (*sequence number*) atau `cmd_seq` pada payload JSON/teks.
- Pada sisi penerima (`onMqttMessage` di [`mqtt_lwt_retained.ino`](content/chapter-15/src/mqtt_lwt_retained/mqtt_lwt_retained.ino) dan [`mqtt_qos_lwt_sim.py`](content/chapter-15/src/mqtt_qos_lwt_sim.py)), simpan `lastHandledCmdSeq` atau himpunan `seen_seqs`. Jika `seq` yang sama datang lagi, tolak efek sampingnya (*idempotent*). Ini sering memberi keandalan setara QoS 2 dengan biaya hanya 2 paket!

### 3. Retained Messages

Secara default, pesan MQTT yang dikirim saat tidak ada Subscriber aktif langsung dibuang oleh Broker. Dengan menyetel **`retain = true`**:
- Broker menyimpan **tepat satu pesan terakhir** per topic.
- Setiap Subscriber baru yang melakukan `SUBSCRIBE` ke topic tersebut **seketika menerima pesan retained tersebut** (berfungsi seperti "status terkini").
- **Peringatan**: Jangan menyalakan `retain=true` untuk topic *command* (seperti `cmd/pump = ON`)! Jika retained aktif, setiap kali ESP32 reboot dan men-subscribe topic perintah, pompa akan menyala ulang secara tak terduga! Gunakan `retain=true` hanya untuk **status/konfigurasi** (`status = online/offline`).
- Untuk menghapus *retained message* dari Broker, kirim pesan ber-payload kosong `""` dengan `retain=true` ke topic tersebut.

### 4. Keepalive & Last Will and Testament (LWT)

Bagaimana dashboard mengetahui jika sebuah ESP32 di kebun tiba-tiba kehabisan baterai atau dicabut paksa?
1. **Keepalive**: Saat `CONNECT`, klien menyepakati interval *keepalive* (misal `30 detik`). Jika tidak ada data dikirim selama 30 detik, klien mengirim paket kecil **`PINGREQ`** dan Broker membalas **`PINGRESP`**.
2. **Last Will (LWT)**: Juga didaftarkan saat paket **`CONNECT`** awal (misalnya `willTopic = "lab/gh01/node-01/status"`, `willMessage = "{\"state\":\"offline\"}"`, `willQoS = 1`, `willRetain = true`).
3. **Kapan LWT Dipicu?** Broker **HANYA** mem-publish LWT apabila koneksi klien putus secara **tidak wajar (*ungraceful*)**—seperti listrik mati, Wi-Fi terputus, atau senyap melebihi **$1{,}5 \times \text{keepalive}$** ($45\text{ detik}$)—**bukan** saat klien mengirim paket `DISCONNECT` normal.

### 5. Sessions & Reconnect Patterns (MQTT 3.1.1 vs MQTT 5.0)

| Fitur | MQTT 3.1.1 | MQTT 5.0 (Standar Terbaru) |
| --- | --- | --- |
| **Kontrol Session** | `cleanSession` boolean (`true` = hapus semua saat putus; `false` = simpan langganan & antrean QoS 1/2) | Dipisah lebih presisi: **`Clean Start`** + **`Session Expiry Interval`** (detik, agar sesi tidak membebani Broker selamanya) |
| **Error Feedback** | Kode return terbatas pada `CONNACK` | **Reason Codes** rinci di `CONNACK`, `PUBACK`, `SUBACK`, `DISCONNECT` |
| **Metadata** | Harus masuk ke dalam payload JSON | **User Properties** (pasangan *key-value* di header) |
| **Efisiensi Topic** | Mengirim string topic utuh di tiap pesan | **Topic Aliases** (ganti string panjang dengan ID integer 2-byte) |
| **Skalabilitas Consumer** | Tidak standar | **Shared Subscriptions** (`$share/group/topic`) untuk *load balancing* |

**Pola Reconnect Penting di ESP32**:
- Jika memakai **`cleanSession = true`**: Broker melupakan seluruh `SUBSCRIBE` saat koneksi putus, sehingga klien **WAJIB memanggil `mqtt.subscribe(...)` ulang** setiap kali `mqtt.connect()` berhasil!
- Jika memakai **`cleanSession = false`** (*Persistent Session*): Broker menyimpan pesan QoS 1/2 yang tertunda selama klien *offline*, tetapi pastikan **`clientId` tetap identik** dan batasi ukuran antrean Broker agar tidak kehabisan memori bila ada ribuan klien mati lama.

### 6. Implementasi Praktis & Simulasi (`mqtt_lwt_retained.ino` & `mqtt_qos_lwt_sim.py`)

- **Firmware ESP32**: [`mqtt_lwt_retained.ino`](content/chapter-15/src/mqtt_lwt_retained/mqtt_lwt_retained.ino) mendaftarkan LWT retained `"offline"`, menerbitkan retained `"online"` setelah terhubung, men-subscribe perintah dengan **QoS 1**, dan mengabaikan duplikat `cmd_seq`. *(Catatan: pustaka `PubSubClient` populer di Arduino mendukung `LWT`, `retain`, dan `subscribe` QoS 0/1, namun `publish()`-nya dibatasi QoS 0. Untuk `publish` QoS 1/2 atau fitur penuh MQTT 5.0 pada ESP32, gunakan komponen **`esp-mqtt`** bawaan ESP-IDF).*
- **Simulasi Python**: [`mqtt_qos_lwt_sim.py`](content/chapter-15/src/mqtt_qos_lwt_sim.py) memverifikasi jumlah paket QoS 0/1/2, penyaringan duplikat `seq=11 (DUP=True)`, perilaku *retained*, serta pemicuan LWT pada `46s > 1.5 * 30s` (`outputs.md`).

### 7. Common Mistakes & Troubleshooting

| Kesalahan | Dampak di Sistem Nyata | Solusi |
| --- | --- | --- |
| Mengirim perintah aktuator (`cmd/relay = ON`) dengan `retain=true` | Setiap kali node reboot, relay otomatis menyala sendiri dari perintah lama! | Gunakan `retain=false` untuk *command*; hapus pesan retained lama dengan payload `""` |
| Mengatur `keepalive = 5 s` untuk ribuan node seluler | Beban *PINGREQ* sangat tinggi dan mudah memicu LWT palsu saat jitter naik | Gunakan *keepalive* realistis ($30\text{--}120\text{ s}$) sesuai kondisi jaringan |
| Memakai `cleanSession = true` tapi hanya `subscribe()` di `setup()` | Setelah reconnect singkat, node mengirim data tapi tidak pernah menerima perintah lagi | Selalu panggil `subscribe()` di dalam blok `if (mqtt.connect(...))` pada loop reconnect! |
| Mengira QoS 2 otomatis menjamin pesan tersimpan di database | QoS hanya menjamin antara klien dan Broker; jika backend subscriber crash sebelum DB commit, data tetap hilang | Gunakan `QoS 1 + deduplikasi seq + ACK setelah DB write` |

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-15/exercises.md)):
1. Menentukan QoS akhir yang diterima Subscriber jika Publisher mengirim QoS 2 dan Subscriber berlangganan QoS 1.
2. Menganalisis insiden "pompa menyala sendiri tiap listrik padam-nyala" akibat kesalahan `retain=true` pada topic perintah.
3. Menghitung total paket TCP aplikasi pada QoS 0 vs QoS 1 vs QoS 2 untuk 1.000 pesan.
4. Menjalankan [`mqtt_qos_lwt_sim.py`](content/chapter-15/src/mqtt_qos_lwt_sim.py) serta Mini Challenge simulasi `cleanSession=false` offline queue.

## Tugas

Rancang **Strategi Keandalan Protokol MQTT (QoS, LWT, Retained & Deduplikasi)** untuk sistem pengawasan ruang server / rumah kaca (detail & rubrik 100 poin di tab **Tugas & Rubrik** — [assignment.md](content/chapter-15/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Bobot | Indikator Penilaian Utama |
| --- | --- | --- |
| Pemilihan tingkat QoS per jenis topic | 25 | Justifikasi QoS 0 vs 1 vs 2 untuk *telemetry*, *alarm*, dan *command* beserta batas library |
| Desain Retained, LWT & Keepalive | 25 | Penggunaan `retain` tepat (status vs command), LWT akurat, serta nilai `keepalive` realistis |
| Deduplikasi & manajemen Session/Reconnect | 30 | Mekanisme idempoten `seq`, penanganan `cleanSession` + re-subscribe, dan perbandingan MQTT 5.0 |
| Simulasi pengujian & kejujuran bukti | 20 | Output skrip/uji terdokumentasi asli serta batasan diverifikasi jujur |

## Ringkasan

- **QoS 0** (1 paket) hemat untuk *telemetry* rutin; **QoS 1** (2 paket) menjamin sampai minimal sekali dan membutuhkan **deduplikasi `seq`**; **QoS 2** (4 paket) paling berat namun tanpa duplikat.
- **Retained Messages** berguna untuk menyajikan status terbaru (`online`/`offline`) kepada Subscriber baru, tetapi **berbahaya jika dipasang pada topic perintah aktuator**.
- **LWT** mendeteksi perangkat mati mendadak setelah $1{,}5 \times \text{keepalive}$ tanpa `DISCONNECT` normal.
- **MQTT 5.0** menyempurnakan 3.1.1 dengan *Session Expiry Interval*, *Reason Codes*, *Topic Aliases*, *User Properties*, dan *Shared Subscriptions*.
- Simulasi QoS, deduplikasi, *retained*, dan LWT telah diverifikasi di Python (`outputs.md`); kompilasi `.ino` menunggu selesainya instalasi core ESP32.

## Referensi

1. OASIS Standard, *MQTT Version 5.0 Specification (Section 4.3 QoS, 3.1.2.11 Session Expiry, 3.1.2.5 Will)*, [https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) (diperiksa 2026-11-11).
2. Espressif Systems, *ESP-IDF ESP-MQTT Client Documentation (QoS 0/1/2 & MQTT 5.0)*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/mqtt.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/mqtt.html) (diperiksa 2026-11-11).
3. Eclipse Foundation, *Mosquitto Manual (`mosquitto.conf` & Persistent Sessions)*, [https://mosquitto.org/man/mosquitto-conf-5.html](https://mosquitto.org/man/mosquitto-conf-5.html) (diperiksa 2026-11-11).

