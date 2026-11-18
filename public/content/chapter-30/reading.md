# Chapter 30 — End-to-End IoT Application Capstone

Setelah menguasai seluruh pilar data, gateway, edge computing, protokol integrasi, penyimpanan deret waktu, dashboarding, keamanan siber, dan siklus hidup pembaruan firmware pada Chapter 21 hingga 29, kita kini menyatukan seluruh komponen tersebut ke dalam sebuah proyek puncak tingkat sarjana: **Scalable IoT Environmental Monitoring & Management Platform**.

Proyek puncak Level 3 ini dirancang dengan pendekatan **Local-First + Simulator-First (Tanpa Cloud Berbayar)**, memungkinkan mahasiswa dan perekayasa sistem untuk menguji dan memvalidasi seluruh skenario arsitektur terdistribusi—mulai dari pendaftaran identitas perangkat keras, isolasi matriks ACL MQTT, validasi skema JSON, pemfilteran sinyal edge, penyimpanan time-series dengan *downsampling rollup*, mesin status peringatan anti-fatigue, rekonsiliasi *Digital Twin*, hingga mitigasi bootloop OTA menggunakan *Automatic Rollback*—secara objektif, terukur, dan sepenuhnya reproducible.

![Arsitektur Platform Capstone Level 3: Field Devices, Edge Gateway, Broker ACL, Storage, dan Operasi Armada](content/chapter-30/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan proyek capstone ini, Anda diharapkan mampu:

1. **Mengintegrasikan Arsitektur Multi-Tier IoT**: Menghubungkan klaster sensor lapangan, gerbang pemroses edge, broker pesan terisolasi ACL, basis data deret waktu, dan platform operasi armada ke dalam satu kesatuan sistem yang harmonis.
2. **Menegakkan Standar Kualitas Data & Keamanan Berlapis**: Memastikan seluruh data yang melintasi sistem tervalidasi oleh JSON Schema ketat, diotentikasi oleh sertifikat digital X.509, dan dibatasi hak aksesnya oleh matriks ACL MQTT.
3. **Mengoptimalkan Throughput & Penyimpanan Data**: Menerapkan pemfilteran deadband dan IQR di sisi edge, serta mengonfigurasi pipeline *downsampling 1-minute rollup* dan pembersihan retensi berkala pada basis data time-series.
4. **Menerapkan Manajemen Peringatan Industri**: Mengonfigurasi mesin status peringatan 4-tahap (`NORMAL` $\rightarrow$ `PENDING` $\rightarrow$ `FIRING` $\rightarrow$ `RESOLVED`) yang dilengkapi pita histeresis dan *rate throttling* untuk melindungi operator dari *alert fatigue*.
5. **Mengeksekusi System Acceptance Test Cases (SATC)**: Memverifikasi 6 skenario penerimaan sistem terintegrasi (Enrollment, Ingestion/Dedup, Time-Series Rollup, Alerting Hysteresis, Twin Drift, dan OTA Rollback) dengan bukti eksekusi empiris yang deterministik.

## Prasyarat

- Menyelesaikan seluruh modul pembelajaran dan latihan dari **Chapter 21 hingga Chapter 29**.
- Memahami konsep arsitektur microservices dan integrasi sistem terdistribusi.
- Memiliki lingkungan runtime Python 3 yang siap mengeksekusi skrip pengujian mandiri.

## Konsep dan teori

### 1. Spesifikasi Arsitektur Sistem Capstone

Platform pemantauan lingkungan kampus cerdas ini terdiri atas tiga zona terdistribusi:

1. **Zona Lapangan (*Field Sensor Cluster*)**:
   - Terdiri atas simpul sensor mikrokontroler (misal: `node-alpha` berbasis ESP32 untuk iklim mikro dan `node-beta` berbasis ESP32-S3 untuk kualitas udara).
   - Menghasilkan aliran telemetri berstempel waktu UTC Unix Epoch, memancarkan denyut jantung (*heartbeat*) berkala, dan mempertahankan kontrol aktuasi lokal mandiri (*local fail-safe hysteresis*).
2. **Zona Gerbang & Keamanan (*Edge Gateway & Security Broker*)**:
   - Broker MQTT (Eclipse Mosquitto lokal) dengan penegakan otorisasi **Access Control List (ACL)** berbasis pola pengguna `%u`.
   - Modul gerbang (*Edge Gateway Processor*) yang memverifikasi kontrak skema JSON, menyaring pesan duplikat (*Idempotency Dedup*), dan meredam transmisi statis menggunakan filter *Deadband*.
   - Integrasi alur kerja visual berbasis event (Node-RED) untuk penyediaan endpoint REST API mikro dan penanganan pengecualian terisolasi (*Catch Node*).
3. **Zona Inti & Operasi (*Platform Core & Operations*)**:
   - **Time-Series Storage (SQLite Engine)**: Menyimpan rekaman mentah 7 hari dan secara kontinu menjalankan agregasi *downsampling 1-minute rollup* untuk retensi tahunan.
   - **Alert State Machine**: Mengevaluasi ambang batas bahaya dengan durasi penahanan $T_{\text{for}} = 5\text{s}$, pita histeresis $1{,}0\,^\circ\text{C}$, dan interval pembatasan notifikasi $15\text{s}$.
   - **Device Twin Registry**: Mengelola inventaris fisik, mendeteksi penyimpangan konfigurasi (*configuration drift*), dan memantau status kesehatan armada (*Online/Degraded/Offline*).
   - **Cryptographic OTA Manager**: Mengelola distribusi firmware bertahap (*canary deployment*), memeriksa keabsahan tanda tangan digital SHA-256/HMAC, dan mengendalikan pemulihan mandiri (*Automatic Rollback*) saat firmware baru mengalami crash runtime.

### 2. Matriks Uji Penerimaan Sistem (SATC Matrix)

Keberhasilan implementasi Capstone Level 3 diukur melalui enam kasus uji penerimaan sistem terintegrasi (*System Acceptance Test Cases*):

| Kode Kasus Uji | Nama Skenario Pengujian | Kriteria Keberhasilan Sistem |
| :--- | :--- | :--- |
| **`SATC-01`** | Device Enrollment & ACL Isolation | Perangkat terdaftar di registri; akses tulis ke topik sendiri diizinkan, akses lintas perangkat (*eavesdropping/spoofing*) diblokir mutlak oleh broker. |
| **`SATC-02`** | Validation, Dedup & Deadband | Payload malformed ditolak skema; pesan retransmisi duplikat disaring oleh cache idempotensi; perubahan kecil di bawah $0{,}5\,^\circ\text{C}$ diredam oleh deadband. |
| **`SATC-03`** | Time-Series Rollup & Retention | Data mentah berurutan dikelompokkan ke jendela 1 menit; metrik agregat (avg, min, max, count) terhitung akurat; data mentah lama terhapus tanpa merusak rollup. |
| **`SATC-04`** | Alerting Pending & Hysteresis | Lonjakan sementara diredam oleh durasi penahanan $5\text{s}$; status menjadi `FIRING` jika panas bertahan; fluktuasi diredam oleh histeresis hingga suhu benar-benar aman. |
| **`SATC-05`** | Digital Twin Drift Reconciliation | Perubahan konfigurasi di cloud memicu bendera `drift = True`; pengiriman konfirmasi *Reported ACK* dari perangkat mengembalikan bendera drift ke `False`. |
| **`SATC-06`** | Secure OTA & Automatic Rollback | Citra biner korup ditolak verifikasi tanda tangan; firmware sah yang mengalami bootloop secara otomatis memicu rollback ke bank lama yang stabil. |

### 3. Eksekusi Skrip Integrasi Terpadu (`capstone_platform.py`)

Skrip [`capstone_platform.py`](content/chapter-30/src/capstone_platform.py) menyatukan seluruh modul yang telah dikembangkan di bab-bab sebelumnya menjadi sebuah lingkungan pengujian otomatis tunggal. Skrip ini menginstansiasi seluruh kelas subsistem di memori lokal, menyimulasikan aliran data waktu nyata, dan mengeksekusi seluruh 6 kasus uji SATC secara deterministik tanpa membutuhkan hardware eksternal atau koneksi cloud berbayar.

### 3.1 Landasan Matematis: Ketersediaan Layanan Pipeline End-to-End & Analisis Latensi P99 (Mathematical Foundations)

Pada integrasi sistem tingkat platform (Level 3 Capstone), parameter kualitas layanan (*Quality of Service*) dievaluasi melalui latensi persentil ke-99 ($P_{99}$) dan ketersediaan komposit:

1. **Distribusi Latensi Persentil ke-99 ($P_{99}$)**:
   Dalam sistem telemetri terdistribusi, rata-rata latensi ($mu$) sering kali menyamarkan lonjakan waktu respons ekstrem (*tail latency*). Nilai persentil ke-99 menyatakan batas atas latensi di mana $99\%$ transaksi berhasil diselesaikan:
   $$
   P_{99} = \inf \{ t \in \mathbb{R} : F(t) \ge 0{,}99 \}
   $$
   di mana $F(t)$ adalah fungsi distribusi kumulatif waktu respons end-to-end (Sensor $\rightarrow$ Broker $\rightarrow$ Database $\rightarrow$ UI).

2. **Kalkulasi Ketersediaan Layanan Komposit (Worked Example)**:
   Arsitektur capstone terdiri atas empat tier independen yang terhubung seri:
   - Ingest Broker (MQTT Cluster): $A_1 = 99{,}95\%$
   - Gateway/Worker Stream Processor: $A_2 = 99{,}90\%$
   - Time-Series Database Cluster: $A_3 = 99{,}99\%$
   - Web Dashboard & Alerting Service: $A_4 = 99{,}90\%$
   Ketersediaan sistem end-to-end $A_{\text{E2E}}$ adalah:
   $$
   A_{\text{E2E}} = A_1 \times A_2 \times A_3 \times A_4 = 0{,}9995 \times 0{,}9990 \times 0{,}9999 \times 0{,}9990 \approx 0{,}9974 \quad (99{,}74\%)
   $$
   Waktu henti (*downtime*) kumulatif per tahun dari platform sistem adalah:
   $$
   T_{\text{down}} = 8760 \times (1 - 0{,}9974) = 8760 \times 0{,}0259 \approx 22{,}78\text{ jam/tahun}
   $$
   Untuk meningkatkan ketersediaan menjadi $99{,}99\%$ (*Four Nines*), tier worker stream processor dan ingest broker wajib mengimplementasikan redundansi aktif paralel (*Active-Active Clustered Nodes*).

## Latihan

1. **Analisis Skalabilitas Platform**:
   Jika platform Capstone ini dikembangkan untuk memantau $1.000$ unit perangkat di seluruh area kampus ITERA dengan frekuensi sampling $5\text{ detik}$:
   - Berapa throughput pesan per detik yang harus ditangani oleh broker MQTT?
   - Mengapa strategi pemfilteran *Deadband* di gerbang edge sangat krusial dalam mencegah kemacetan jaringan pada skala tersebut?
2. **Evaluasi Keamanan Terpadu**:
   Jelaskan bagaimana kombinasi antara sertifikat identitas X.509 pada protokol mTLS, penegakan matriks ACL topik Mosquitto, dan penandatanganan firmware kriptografis pada OTA bersama-sama membentuk arsitektur keamanan *Defense-in-Depth* yang tahan terhadap serangan siber modern.
3. **Manajemen Kegagalan Komprehensif**:
   Sebutkan tiga titik kegagalan (*Single Points of Failure*) yang paling berisiko terjadi pada sistem IoT terintegrasi dan jelaskan mekanisme penanganan kesalahan mandiri (*self-healing*) yang telah diimplementasikan pada arsitektur Capstone ini untuk mengatasinya.

## Tugas

Bangun, jalankan, dan evaluasi platform pemantauan lingkungan terintegrasi menggunakan skrip [`capstone_platform.py`](content/chapter-30/src/capstone_platform.py):

1. **Integrasi Seluruh Subsistem**:
   Pastikan skrip memuat implementasi lengkap dari `DeviceTwinRegistry`, `TopicAclAuthorizer`, `EdgeGatewayProcessor`, `CapstoneTimeSeriesStorage`, `CapstoneAlertEngine`, dan `CapstoneOtaManager`.
2. **Eksekusi 6 Kasus Uji Penerimaan (SATC-01 hingga SATC-06)**:
   Jalankan skrip penerimaan sistem dan buktikan bahwa seluruh 6 skenario pengujian lulus evaluasi (*100% Passed*).
3. **Dokumentasi Hasil Uji & Analisis Teknis**:
   Catat log keluaran terminal pada berkas [`outputs.md`](content/chapter-30/outputs.md), lalu susun laporan analisis teknis yang membedah keandalan sistem pada masing-masing tahapan uji.

### Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Arsitektur Integrasi & Kualitas Kode** | 35 | Seluruh 6 subsistem terintegrasi harmonis; kode modular, bebas redundansi, dan mengimplementasikan prinsip local-first & simulator-first. |
| **Ketepatan Eksekusi SATC (Kebenaran Fungsional)** | 35 | Seluruh 6 kasus uji penerimaan sistem (SATC-01 sampai SATC-06) berhasil dieksekusi dan lolos verifikasi tanpa kesalahan logika. |
| **Analisis Keandalan & Dokumentasi Teknis** | 30 | Bukti eksekusi terdokumentasi lengkap dan deterministik; analisis teknis membedah trade-off arsitektur dan mitigasi kegagalan secara mendalam. |

## Ringkasan

1. **Sinergi Ujung-ke-Ujung**: Platform Capstone Level 3 membuktikan bahwa integrasi data, gateway edge, penyimpanan teroptimasi, keamanan berlapis, dan manajemen armada dapat diwujudkan secara kokoh dan mandiri tanpa ketergantungan cloud berbayar.
2. **Keandalan Deterministik**: Melalui verifikasi 6 kasus uji SATC, sistem membuktikan kemampuannya menyaring anomali, mempertahankan ketersediaan armada, dan memulihkan diri secara mandiri dari kegagalan firmware.
3. **Kesiapan Skala Industri**: Fondasi arsitektur yang dibangun pada Level 3 memberikan pijakan kokoh untuk melangkah ke analisis data tingkat lanjut, machine learning edge, dan sistem otonom cerdas pada Level 4.

## Referensi
- Dean, J., & Barroso, L. A., *The Tail at Scale*, Communications of the ACM, Vol. 56 No. 2, 2013.
- IEEE Std 1451.4, *Standard for A Smart Transducer Interface for Sensors and Actuators*, IEEE.

1. Sinclair, I. *Sensors and Transducers (3rd Edition)*. Newnes Elsevier.
2. Bass, L., Clements, P., & Kazman, R. *Software Architecture in Practice (4th Edition)*. Addison-Wesley Professional.
3. Internet of Things Consortium. *End-to-End IoT Reference Architecture and Acceptance Testing Guidelines*.
