# Chapter 21 — IoT Data Models, Telemetry & Event Design

Dalam sistem IoT berskala industri, data tidak sekadar barisan byte yang dikirimkan melewati socket TCP atau broker MQTT. Tanpa standardisasi struktur, semantik satuan, dan kejelasan intensi komunikasi, sistem backend akan segera mengalami kekacauan integrasi (*data pipeline breakdown*). Sebuah sistem IoT yang matang memisahkan secara tegas antara **aliran telemetri berkala (telemetry)**, **peristiwa diskrit kritis (event)**, **perintah kendali jarak jauh (command)**, dan **kondisi sinkronisasi perangkat (device twin/state)**.

Bab ini menyajikan fondasi arsitektur data models, perancangan kontrak JSON Schema, penanganan stempel waktu UTC presisi tinggi, versioning skema evolutif, mitigasi pesan duplikat (*idempotency*), serta perbandingan efisiensi payload antara representasi tekstual dan kompresi biner.

![Taksonomi Data IoT: Telemetry, Event, Command, dan Device State](content/chapter-21/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, mahasiswa dan praktisi IoT diharapkan mampu:

1. **Mengklasifikasikan Taksonomi Pesan**: Membedakan karakteristik ontologis antara *telemetry*, *event*, *command*, dan *digital twin state* beserta implikasi toleransi kehilangan data (*loss-tolerance* vs *loss-sensitivity*).
2. **Merancang Skema Validasi Formal**: Menyusun kontrak data berbasis **JSON Schema Draft-07 / 2020-12** lengkap dengan batasan numerik fisik, tipe data primitif, dan kriteria validasi ketat (*strict validation*).
3. **Menerapkan Standar Waktu Universal**: Mengelola stempel waktu (*timestamps*) berbasis Unix Epoch integer dan representasi ISO 8601 UTC guna mencegah ambiguitas zona waktu (*timezone drift*) dan efek lompatan kabisat.
4. **Membangun Pipeline Idempotensi**: Menerapkan mekanisme de-duplikasi pesan pada sisi penerima menggunakan kunci gabungan `(device_id, sequence_number)` atau `event_id` dengan jendela *cache* berbasis waktu (TTL).
5. **Menganalisis Efisiensi Serialisasi**: Menghitung *overhead* protokol dan rasio efisiensi byte antara formatted JSON, minified JSON, serta binary packing berbasis `struct` atau CBOR untuk jaringan berkapasitas sempit (*LPWAN / cellular narrowband*).

## Prasyarat

- Memahami arsitektur protokol MQTT (Publish/Subscribe, QoS 0/1/2, Retained, LWT) dari [Chapter 14](chapter-14) dan [Chapter 15](chapter-15).
- Memahami konsep serialisasi JSON pada mikrokontroler dari [Chapter 13](chapter-13).
- Memahami dasar manipulasi struktur data dan pemrosesan string Python 3.

## Konsep dan teori

### 1. Taksonomi Komunikasi Data IoT

Dalam arsitektur terdistribusi, setiap pesan yang melintasi jaringan harus memiliki tujuan dan sifat semantik yang jelas:

| Dimensi | Telemetry Stream | Discrete Event | Actionable Command | Device Twin State |
| :--- | :--- | :--- | :--- | :--- |
| **Definisi** | Deret waktu pengukuran sensor berkala | Notifikasi kejadian penting/anomali | Instruksi aksi dari sistem luar | Rekonsiliasi kondisi perangkat |
| **Frekuensi** | Berkala (misal: tiap $1\text{–}10\text{ detik}$) | Asinkron / berbasis interupsi | Sesuai kebutuhan kendali operator | Saat perubahan konfigurasi/boot |
| **Toleransi Hilang** | Cenderung *loss-tolerant* (data berikutnya segera tiba) | Sangat *loss-sensitive* (tidak boleh hilang) | Memerlukan *Delivery Guarantee* (QoS 1) | Memerlukan persistensi (*retained*) |
| **Topik MQTT Contoh** | `iot/tenant/dev01/telemetry` | `iot/tenant/dev01/event/critical` | `iot/tenant/dev01/cmd/relay` | `iot/tenant/dev01/state/report` |
| **Arah Aliran** | Node $\rightarrow$ Broker $\rightarrow$ Ingestion | Node $\rightarrow$ Broker $\rightarrow$ Alerting | Controller $\rightarrow$ Node | Dua arah (*Desired* $\leftrightarrow$ *Reported*) |

### 2. Standar Penamaan Topik dan Payload

Penamaan topik MQTT harus mencerminkan struktur hierarki logis tanpa menyebabkan fragmentasi berlebih pada indeks pohon broker:

$$\text{Topic Structure} = \text{tenant\_id} / \text{site\_id} / \text{device\_id} / \text{message\_type} [ / \text{sub\_category} ]$$

Contoh praktis:
- Telemetri iklim mikro: `lab-iot/gedung-a/esp32-node01/telemetry`
- Alarm sensor gas bocor: `lab-iot/gedung-a/esp32-node01/event/gas_leak`
- Perintah kalibrasi nol: `lab-iot/gedung-a/esp32-node01/cmd/calibrate`

### 3. Timestamping dan Penanganan Skew Waktu

Setiap sampel data wajib menyertakan stempel waktu pengukuran pada saat akuisisi fisik terjadi di perangkat edge ($t_{\text{capture}}$), bukan waktu saat pesan diterima oleh server cloud ($t_{\text{ingest}}$):

$$t_{\text{latency}} = t_{\text{ingest}} - t_{\text{capture}}$$

1. **Format Timestamp**: Gunakan Unix Epoch UTC dalam detik integer (atau milidetik jika membutuhkan resolusi tinggi).
2. **Kualitas Waktu (*Time Quality*)**: Jika perangkat belum berhasil melakukan sinkronisasi NTP, tandai flag `time_synced: false` agar ingestion pipeline tidak mencampuradukkan data stempel awal `1970-01-01` dengan deret waktu aktif.

### 4. Idempotensi dan Pencegahan Pesan Ganda

Dalam jaringan nirkabel, mekanisme *retransmission* (seperti MQTT QoS 1) menjamin *at-least-once delivery*. Konsekuensinya, pesan yang sama dapat tiba lebih dari satu kali (*duplicate delivery*).

Untuk menjamin eksekusi yang **idempoten** (operasi yang dieksekusi berulang kali menghasilkan efek sistem yang sama):
- Setiap paket menyertakan urutan sekuensial unik `seq` atau UUID `event_id`.
- Edge gateway atau broker ingestion memelihara tabel penjejak pesan (*deduplication cache*) dengan batas waktu kedaluwarsa ($T_{\text{TTL}}$):

$$\text{Key} = \text{device\_id} \oplus \text{message\_id}$$

Jika pasangan $\text{Key}$ telah tercatat dalam rentang $t \le T_{\text{TTL}}$, paket diklasifikasikan sebagai duplikat dan diabaikan dari pemrosesan bisnis (*discard*), tetapi tetap di-ACK ke broker.

### 5. Kompresi dan Efisiensi Payload

Pada jaringan seluler (NB-IoT/LTE-M) atau LoRaWAN di mana kuota transmisi sangat dibatasi, format JSON mentah sering kali menyumbang redundansi berlebih karena nama-nama field tekstual berulang.

Sebagai contoh perbandingan untuk paket telemetri 4 metrik:
1. **JSON Indented**: $\sim 209\text{ byte}$
2. **JSON Minified**: $\sim 157\text{ byte}$ (penghematan $\sim 25\%$)
3. **Packed Binary Struct**: $\sim 32\text{ byte}$ (penghematan $\sim 80\text{–}85\%$)

Di mana skema biner dapat dipadatkan memakai skala integer tetap (*fixed-point arithmetic*), seperti $T_{\text{scaled}} = \text{int16}(T \times 100)$ dengan resolusi $0{,}01\,^\circ\text{C}$.

## Latihan

1. **Analisis Taksonomi**:
   Sebuah stasiun cuaca mengirimkan suhu setiap 30 detik. Tiba-tiba sensor mendeteksi kecepatan angin melebihi batas badai ($>80\text{ km/jam}$) dan harus segera memicu alarm darurat. Tentukan klasifikasi kedua paket tersebut (apakah telemetry atau event) dan jelaskan alasan perbedaannya dari segi QoS dan retensi.
2. **Perancangan Schema**:
   Tuliskan potongan JSON Schema untuk memvalidasi payload sensor getaran industri (*accelerometer 3-axis*) yang memuat parameter `accel_x`, `accel_y`, dan `accel_z` dengan rentang batas fisik $-16{,}0\text{ g}$ hingga $+16{,}0\text{ g}$.
3. **Analisis Idempotensi**:
   Jika sebuah perintah `{"cmd":"restart"}` dikirimkan dengan QoS 1 dan terjadi *network disconnect* tepat setelah mikrokontroler mengeksekusi restart namun sebelum ACK terkirim, jelaskan bagaimana skema nomor token perintah mencegah terjadinya perulangan reboot tak berujung (*bootloop*).

## Tugas

Buatlah implementasi skrip Python mandiri yang melakukan validasi komprehensif terhadap aliran telemetri IoT dan de-duplikasi pesan duplikat:

1. **Modul Schema Validator**:
   Implementasikan validator data yang menolak secara otomatis setiap payload yang melanggar batasan tipe data, rentang numerik, atau kelengkapan field wajib sesuai kontrak JSON Schema.
2. **Modul Deduplikasi Idempotensi**:
   Bangun kelas pipeline `IdempotencyDeduplicator` dengan kapasitas memori terbatas (LRU/TTL) yang mampu mendeteksi dan mengeliminasi pesan ganda dalam jendela waktu $60\text{ detik}$.
3. **Benchmark Efisiensi Payload**:
   Bandingkan ukuran byte antara formatted JSON, compact minified JSON, dan binary packing (menggunakan modul `struct`).

### Rubrik Penilaian

| Kriteria | Bobot | Deskripsi Teknis |
| :--- | :---: | :--- |
| **Kebenaran Skema & Validasi** | 35% | Kontrak schema didefinisikan secara lengkap; validator menolak payload malformed dengan pesan kesalahan terstruktur yang eksplisit. |
| **Mekanisme Idempotensi & TTL** | 35% | Pipeline deduplikasi berhasil menyaring duplikat dalam batas TTL dan secara otomatis membersihkan entri usang (*eviction*). |
| **Analisis Efisiensi & Dokumentasi** | 30% | Komparasi ukuran data dilakukan secara matematis dan empiris; kode terdokumentasi rapi, modular, dan lulus seluruh uji otomatis. |

## Ringkasan

1. **Pemisahan Semantik**: Memisahkan *telemetry* (kontinu, loss-tolerant), *event* (diskrit, loss-sensitive), *command* (aksi, butuh ACK), dan *state* (kondisi twin) adalah fondasi arsitektur data IoT modern.
2. **Validasi Kontrak**: Validasi JSON Schema di sisi edge/ingestion mencegah data korup masuk ke penyimpanan jangka panjang dan merusak integritas analitik.
3. **Stempel Waktu UTC**: Penggunaan waktu Unix UTC integer mutlak diperlukan untuk mencegah ambiguitas lokal dan masalah penyesuaian zona waktu.
4. **Idempotensi**: Idempotensi berbasis `(device_id, sequence_number)` menjamin keandalan sistem terhadap pengiriman ulang jaringan tanpa efek samping ganda.
5. **Efisiensi Payload**: Serialisasi biner terkompresi mampu memangkas ukuran transmisi hingga $>80\%$ dibanding JSON mentah pada tautan berdaya rendah.

## Referensi

1. Internet Engineering Task Force (IETF). *RFC 8610: Concise Data Definition Language (CDDL) and CBOR (RFC 8949)*.
2. JSON Schema Organization. *JSON Schema Validation: A Vocabulary for Structural Validation of JSON (Draft 2020-12)*. https://json-schema.org/
3. OASIS Standard. *MQTT Version 5.0 / 3.1.1 Specification*. Section 3: MQTT Control Packets.
