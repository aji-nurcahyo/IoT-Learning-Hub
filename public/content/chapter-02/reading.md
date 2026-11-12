# Chapter 02 — IoT Architecture, Use Cases & System Requirements

## Overview

Sebuah proyek IoT jarang gagal karena pengembang tidak bisa menulis kode membaca sensor; sebagian besar kegagalan di lapangan terjadi karena **arsitektur tidak diturunkan dari kebutuhan sistem (*system requirements*)**. Memilih Wi-Fi untuk node bertenaga baterai di perkebunan sejauh 2 kilometer, atau meletakkan logika *safety alarm* sepenuhnya di server *cloud*, adalah kesalahan arsitektur yang tidak bisa diperbaiki sekadar dengan optimasi kode.

Chapter ini membahas cara merancang arsitektur IoT secara sistematis: mulai dari model berlapis (*three-layer* dan *five-layer architecture*), pemisahan kebutuhan fungsional dan non-fungsional, penetapan batas sistem (*system boundaries*), analisis *trade-off* antara *Edge* dan *Cloud*, hingga penyusunan *use-case diagram* dan *block diagram* melalui studi kasus **Sistem Monitoring Suhu Terdistribusi**.

## Prasyarat

- Disarankan telah mempelajari [Chapter 01 — Introduction to the Internet of Things](#/chapter/1) untuk memahami enam komponen ekosistem IoT serta aliran *uplink/downlink*.
- Kemampuan dasar aljabar untuk menyusun anggaran *bandwidth*, kapasitas memori *buffer*, dan batas latensi.

## Tujuan pembelajaran

Setelah menyelesaikan chapter ini, mahasiswa mampu:

1. **Membandingkan** model *three-layer* dan *five-layer IoT architecture* serta tanggung jawab masing-masing lapisan (*Device, Network, Edge, Platform, Application*).
2. **Menyusun** daftar *functional requirements* dan *non-functional requirements* (latensi, daya, *bandwidth*, jangkauan, ketersediaan, biaya) secara terukur untuk satu skenario IoT.
3. **Menentukan** batas sistem (*system boundaries*) dan mengevaluasi *trade-off* pemrosesan di *Edge* versus *Cloud*.
4. **Merancang** *use-case diagram*, *block diagram*, dan spesifikasi kebutuhan untuk studi kasus sistem monitoring suhu terdistribusi.

## Konsep dan teori

### 1. Three-Layer vs Five-Layer IoT Architecture

Dalam literatur rekayasa IoT, arsitektur sistem sering direpresentasikan menggunakan dua model utama:

**A. Three-Layer Architecture (Model Klasik)**
1. **Perception Layer**: Lapisan fisik berisi *Sensor*, *Actuator*, dan *Microcontroller* yang berinteraksi langsung dengan lingkungan.
2. **Network Layer**: Lapisan pengangkutan data dari node menuju sistem pemroses (Wi-Fi, BLE, LoRa, Seluler, IP routing).
3. **Application Layer**: Lapisan penyaji layanan bagi pengguna akhir (visualisasi rumah pintar, *smart agriculture*, pemantauan energi).

Model tiga lapis sangat baik untuk menjelaskan ide dasar, tetapi **terlalu kasar untuk desain teknik**. Ia menyembunyikan peran *Gateway*, *buffering* lokal, manajemen perangkat, dan *data pipeline*. Karena itu, praktik rekayasa modern memakai **Five-Layer Architecture**:

| Lapisan (5-Layer) | Tanggung Jawab Inti | Contoh Komponen / Teknologi |
| --- | --- | --- |
| **1. Device / Perception** | Akuisisi sinyal fisik, konversi ADC, *fail-safe* lokal | Node ESP32 + sensor suhu, relay darurat |
| **2. Network / Transport** | Pengiriman paket antar-hop, framing, keandalan tautan | BLE, Sub-GHz/LoRa, Wi-Fi, Ethernet, 4G LTE |
| **3. Edge / Middleware** | Agregasi jendela waktu, penyaringan noise, *store-and-forward* | Gateway lokal, edge broker, aturan respons cepat |
| **4. Platform / Processing** | Ingest skala besar, validasi skema, penyimpanan *time-series* | MQTT Broker, Time-Series DB, rule engine |
| **5. Application / Business** | Antarmuka operator, pelaporan SLA, integrasi ERP/alert | Dashboard NOC, sistem tiket teknisi, grafik tren |

### 2. Functional vs Non-Functional Requirements

Sebelum menggambar skema rangkaian atau memilih papan *Microcontroller*, arsitek sistem memisahkan kebutuhan menjadi dua kategori:

- **Functional Requirements ("Apa yang harus dilakukan sistem")**:
  - Contoh: *"Node membaca suhu setiap 5 detik, mengirim ringkasan tiap 60 detik, dan menyalakan buzzer lokal jika suhu melebihi $8\,^\circ\text{C}$ selama lebih dari 30 detik."*
- **Non-Functional Requirements ("Seberapa baik dan dalam batas apa sistem bekerja")**:
  - **Latency**: Batas waktu maksimum dari kejadian fisik hingga respons (misalnya $< 100\text{ ms}$ untuk proteksi lokal, $< 10\text{ s}$ untuk notifikasi dashboard).
  - **Power**: Anggaran konsumsi arus rata-rata dan umur baterai target (misalnya bertahan 6 bulan pada baterai LiFePO4 3000 mAh, atau catu daya DC 5 V permanen).
  - **Bandwidth**: Kebutuhan laju data *uplink/downlink* agar sesuai kuota seluler atau kapasitas kanal radio.
  - **Range & Topology**: Jarak fisik antar-node dan *Gateway* serta kondisi halangan (dinding beton, kanopi kebun, ruang logam).
  - **Availability & Reliability**: Persentase waktu operasi yang diharapkan (misal $99{,}5\%$) dan perilaku *offline buffering* saat jaringan terganggu.
  - **Cost**: Biaya per node (*BOM*), biaya *Gateway*, serta biaya operasional langganan SIM/cloud (*OPEX*).

Menulis kebutuhan non-fungsional tanpa angka (misalnya *"sistem harus cepat dan hemat daya"*) **tidak dapat diuji**. Selalu nyatakan target numerik beserta kondisi ukurnya.

### 3. System Boundaries & Aliran Data

**System boundary** menetapkan komponen mana yang berada di bawah kendali desain Anda, dan mana yang merupakan entitas eksternal (misalnya operator seluler, jaringan PLN, atau pengguna akhir).

Diagram berikut memperlihatkan pemetaan arsitektur lima lapis beserta batas antara *Edge* dan *Cloud*:

![Diagram arsitektur lima lapis IoT dan batas Edge vs Cloud](content/chapter-02/diagram.svg)

Memahami batas sistem menjawab pertanyaan krusial:
- *Jika koneksi antara Gateway (Lapisan 3) dan Cloud Platform (Lapisan 4) terputus, fitur apa yang harus tetap berjalan?*
- *Antarmuka kontrak (API / skema pesan) apa yang menjembatani setiap batas lapisan?*

### 4. Trade-Off Edge Computing vs Cloud Computing

Memindahkan seluruh data mentah ke *Cloud* bukan selalu pilihan terbaik. Keputusan menempatkan pemrosesan di *Edge* atau *Cloud* mengikuti matriks *trade-off* berikut:

| Kriteria Evaluasi | Pemrosesan di Edge / Node | Pemrosesan di Cloud Platform |
| --- | --- | --- |
| **Latensi respons** | Sangat rendah & deterministik (milidetik) | Bergantung kondisi WAN (ratusan ms hingga detik) |
| **Ketahanan saat internet mati** | Tetap beroperasi (*autonomous local loop*) | Terhenti kecuali ada *fallback* lokal |
| **Penggunaan bandwidth uplink** | Hemat (kirim agregat: min/avg/max atau anomali) | Tinggi (kirim seluruh sampel mentah) |
| **Kapasitas komputasi & arsip** | Terbatas RAM/Flash dan daya | Hampir tak terbatas untuk analitik historis lintas lokasi |
| **Kompleksitas pemeliharaan** | Pembaruan *Firmware* tersebar di banyak node | Pembaruan terpusat di satu server |

**Prinsip Emas Desain**: Jalankan **logika keselamatan, penyaringan *noise*, dan agregasi interval** sedekat mungkin dengan *Edge/Device*; simpan **arsip jangka panjang, korelasi multi-lokasi, dan dashboard bisnis** di *Cloud*.

### 5. Use-Case Diagram & Block Diagram

Dalam dokumentasi teknik, arsitektur diwujudkan melalui dua pandangan pelengkap:

1. **Use-Case Diagram (Pandangan Aktor & Perilaku)**:
   Menunjukkan aktor eksternal (Operator Gudang, Teknisi Pemeliharaan, Sistem Pendingin) dan interaksi fungsionalnya dengan sistem:
   ```text
   +-------------------------------------------------------+
   |         Sistem Monitoring Suhu Terdistribusi          |
   |                                                       |
   |  (Pantau Tren Suhu) <--- [Operator Gudang]            |
   |  (Konfigurasi Ambang) <-- [Teknisi NOC]               |
   |  (Terima Alert SLA) ----> [Teknisi NOC]               |
   |  (Picu Alarm Lokal) ----> [Buzzer / Sistem Pendingin] |
   +-------------------------------------------------------+
   ```
2. **Block Diagram (Pandangan Aliran Sinyal & Antarmuka)**:
   Menunjukkan blok fungsional beserta protokol/sinyal penghubung:
   ```text
   [Sensor Suhu] --(Analog/I2C)--> [ESP32 Node] --(Wi-Fi/Sub-GHz)--> [Edge Gateway]
                                        |                                  |
                                  (GPIO/Relay)                       (HTTPS/MQTT)
                                        v                                  v
                                 [Alarm Lokal]                     [Cloud Platform]
   ```

### 6. Model Matematis Anggaran Bandwidth & Offline Buffer

Untuk membandingkan skenario *Direct-to-Cloud* dan *Edge Aggregation*, hitung volume total di jaringan (*wire volume*) dengan memasukkan *protocol overhead* $H$ byte per paket di samping *payload* $B$ byte:

$$
V_{\text{wire/hari}} = M \times \frac{86400}{\Delta t_{\text{uplink}}} \times (B + H)
$$

Jika *Gateway* harus menyimpan data *telemetry* selama gangguan koneksi berdurasi $T_{\text{outage}}$ jam, maka kapasitas minimum *offline buffer* $C_{\text{buf}}$ adalah:

$$
C_{\text{buf}} = M \times \frac{T_{\text{outage}} \times 3600}{\Delta t_{\text{uplink}}} \times B \text{ (byte)}
$$

### 7. Studi Kasus & Worked Example: Monitoring Suhu Terdistribusi

**Skenario**: Sebuah fasilitas penyimpanan rantai dingin (*cold-chain*) dan ruang server memiliki **40 titik sensor** ($M = 40$) di 4 ruangan. Sensor dibaca tiap 5 detik untuk mendeteksi kenaikan suhu cepat (target batas aman $+2\dots +8\,^\circ\text{C}$). Backhaul internet memakai koneksi seluler dengan risiko gangguan hingga $T_{\text{outage}} = 6\text{ jam}$. Asumsikan *protocol overhead* TCP/IP/MQTT sebesar $H = 64\text{ byte}$ per paket.

Bandingkan dua rancangan:
- **Opsi A (Direct-to-Cloud Raw)**: Setiap node mengirim $B = 140\text{ byte}$ langsung ke *Cloud* setiap $\Delta t_{\text{uplink}} = 5\text{ s}$.
- **Opsi B (Edge Gateway Aggregation)**: Node mengirim sampel lokal ke *Gateway*, lalu *Gateway* merangkum jendela 60 detik (`min, avg, max, alarm_flag`, $B = 220\text{ byte}$) setiap $\Delta t_{\text{uplink}} = 60\text{ s}$ dan menahan *buffer* saat internet putus.

**Hasil Analisis via Skrip [`requirements_budget.py`](content/chapter-02/src/requirements_budget.py)** (telah dieksekusi nyata; log di [`outputs.md`](content/chapter-02/outputs.md)):
- **Opsi A**: $691.200\text{ paket/hari}$, volume jaringan $134{,}47\text{ MiB/hari}$ ($\approx 4{,}03\text{ GiB/bulan}$), membutuhkan buffer $23.625\text{ KiB}$ ($\approx 23{,}1\text{ MiB}$), dan latensi kendali jika memutar lewat *Cloud* mencapai $850\text{ ms}$ (serta gagal total jika internet mati).
- **Opsi B**: $57.600\text{ paket/hari}$, volume jaringan $15{,}60\text{ MiB/hari}$ (penghematan **88,4%** beban *uplink*), kebutuhan buffer 6 jam hanya $3.093{,}8\text{ KiB}$ ($\approx 3{,}02\text{ MiB}$), serta latensi alarm darurat lokal turun menjadi **$25\text{ ms}$** ($34\times$ lebih cepat dan tetap aktif saat internet putus).

Contoh data ringkasan *Edge* dapat dilihat pada [`telemetry.csv`](content/chapter-02/telemetry.csv) (`source=synthetic`).

### 8. Kesalahan Umum & Troubleshooting Arsitektur

| Kesalahan Desain | Gejala di Lapangan | Solusi Arsitektural |
| --- | --- | --- |
| Memilih Wi-Fi untuk sensor baterai jarak jauh | Baterai habis dalam hitungan hari, sinyal sering *drop* | Evaluasi BLE/Sub-GHz/LoRa atau catu daya DC tetap + *Gateway* |
| Tidak membatasi ukuran *offline buffer* | RAM/Flash *Gateway* penuh saat gangguan WAN panjang lalu *crash* | Gunakan *ring buffer* (FIFO menimpa data terlama atau downsampling) |
| Menggabungkan seluruh logika bisnis ke *Firmware* node | Setiap ubah aturan dashboard harus mem-flash ulang 40 node | Pisahkan *local safety threshold* di node dan *business rules* di platform |
| Mengabaikan *overhead* protokol & *retransmission* | Kuota data seluler jebol jauh melampaui hitungan ukuran JSON | Hitung $(B + H)$ dan tambahkan margin $20\text{--}30\%$ untuk *retry*/TLS |

### 9. Aplikasi di Dunia Nyata

- **Telecommunications NOC & Edge Sites**: Operator seluler memantau puluhan kabinet *outdoor* menggunakan *Edge Gateway* lokal agar alarm suhu tinggi tetap membunyikan sirene/kipas cadangan meski link *backhaul* sedang *down*.
- **Cold-Chain Logistics & Farmasi**: Gudang vaksin menggunakan arsitektur 5-lapis dengan *store-and-forward* wajib agar tidak ada celah data (*data gap*) selama audit kepatuhan regulasi.
- **Smart Greenhouse Multi-Blok**: Sensor tanah mengirim data setiap menit ke *Edge Controller* lokal untuk menyalakan katup irigasi secara deterministik, sementara ringkasan harian dikirim ke *Cloud* untuk analisis agronomis.

## Latihan

Latihan lengkap tersedia pada tab **Exercises** ([exercises.md](content/chapter-02/exercises.md)):
1. Pemetaan arsitektur 5-lapis dan penentuan *system boundary* untuk kasus *smart irrigation*.
2. Penyusunan tabel *functional* vs *non-functional requirements* dengan angka terukur.
3. Analisis perhitungan *bandwidth* & *outage buffer* menggunakan [`requirements_budget.py`](content/chapter-02/src/requirements_budget.py).
4. Mini challenge memodifikasi parameter skrip untuk mengevaluasi skenario 100 node berkuota seluler terbatas.

## Tugas

Rancang **Dokumen Arsitektur & Spesifikasi Kebutuhan Sistem IoT** untuk skenario kebutuhan terukur (tersedia pada tab **Tugas & Rubrik** — [assignment.md](content/chapter-02/assignment.md)).

Ringkasan **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Poin | Indikator Penilaian Utama |
| --- | --- | --- |
| Spesifikasi kebutuhan fungsional & non-fungsional | 25 | Kejelasan fitur dan target numerik latensi, daya, bandwidth, jangkauan, ketersediaan, biaya |
| Desain arsitektur 5-lapis & system boundaries | 25 | Ketepatan pembagian tanggung jawab tiap lapis, diagram blok, dan *use-case diagram* |
| Analisis trade-off Edge vs Cloud & perhitungan kapasitas | 25 | Justifikasi penempatan pemrosesan serta perhitungan volume data & *offline buffer* |
| Skenario kegagalan, fail-safe & referensi | 25 | Penanganan putus jaringan/daya, keamanan dasar, dan referensi primer yang valid |

## Ringkasan

- Model **five-layer architecture** (*Device, Network, Edge, Platform, Application*) memperjelas peran *Edge/Middleware* yang sering terabaikan pada model 3-lapis.
- Kebutuhan sistem harus dipisah menjadi *functional* dan *non-functional requirements* dengan batas numerik yang dapat diuji (latensi, daya, *bandwidth*, jangkauan, ketersediaan, biaya).
- Pada studi kasus 40 node monitoring suhu, pemindahan agregasi ke *Edge Gateway* memangkas volume *uplink* hingga **88,4%** dalam model matematis `requirements_budget.py` sekaligus menjaga respons darurat tetap aktif secara lokal saat jaringan WAN terputus.

## Referensi

1. National Institute of Standards and Technology (NIST), *Considerations for Managing Internet of Things (IoT) Cybersecurity and Privacy Risks (NISTIR 8228)*, [https://csrc.nist.gov/publications/detail/nistir/8228/final](https://csrc.nist.gov/publications/detail/nistir/8228/final) (diperiksa 2026-11-10).
2. Espressif Systems, *ESP-IDF Programming Guide — Application & Architecture Overview*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html) (diperiksa 2026-11-10).
3. OASIS Standard, *MQTT Version 5.0 Specification*, [https://mqtt.org/mqtt-specification/](https://mqtt.org/mqtt-specification/) (diperiksa 2026-11-10).
4. Raspberry Pi Foundation, *Raspberry Pi Documentation (Edge Gateway Reference)*, [https://www.raspberrypi.com/documentation/](https://www.raspberrypi.com/documentation/) (diperiksa 2026-11-10).

