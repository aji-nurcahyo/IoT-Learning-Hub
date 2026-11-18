# Chapter 28 — IoT Security: Identity, TLS & Access Control

Dalam ekosistem Internet of Things, celah keamanan pada satu sensor berharga murah dapat menjadi pintu masuk bagi penyerang untuk meretas seluruh infrastruktur jaringan kampus atau fasilitas industri. Jutaan perangkat IoT yang terhubung tanpa enkripsi atau menggunakan kata sandi bawaan pabrik (*default hardcoded credentials*) telah berulang kali disalahgunakan menjadi jaringan botnet masif (seperti insiden terkenal *Mirai Botnet*).

Membangun sistem IoT yang aman tidak cukup hanya dengan mengandalkan keamanan perimeter (seperti firewall router). Diperlukan pendekatan **Pertahanan Berlapis (*Defense-in-Depth*)** dan **Zero Trust**: setiap simpul harus memiliki identitas kriptografis unik berbasis sertifikat digital X.509, seluruh lalu lintas data wajib dienkripsi menggunakan protokol **Mutual TLS (mTLS v1.3)**, dan otorisasi topik pada broker pesan harus dibatasi secara ketat menggunakan **Access Control List (ACL)** berdasarkan prinsip hak akses terkecil (*Principle of Least Privilege*).

![Arsitektur Keamanan Berlapis IoT: PKI X.509, mTLS v1.3, dan Matriks Otorisasi MQTT ACL](content/chapter-28/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Menerapkan Pemodelan Ancaman STRIDE**: Mengidentifikasi potensi celah keamanan siber pada sistem IoT (*Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege*).
2. **Mengelola Public Key Infrastructure (PKI) & Sertifikat X.509**: Memahami rantai kepercayaan kriptografis (*Certificate Authority / CA chain*), membedakan pasangan kunci asimetris (*Private/Public Key*), dan memvalidasi masa berlaku sertifikat.
3. **Menerapkan Mutual TLS (mTLS v1.3)**: Menjelaskan proses jabat tangan (*handshake*) otentikasi dua arah di mana broker memverifikasi sertifikat mikrokontroler dan mikrokontroler memverifikasi keaslian broker.
4. **Merancang Matriks Otorisasi Topik MQTT (ACL)**: Menyusun aturan Access Control List berbasis pola pengguna (`%u`) untuk mengisolasi akses telemetri dan kendali antar perangkat secara mutlak.
5. **Menerapkan Praktik Keamanan Standar NIST IR 8259**: Menegakkan manajemen rahasia yang aman (*secrets management*), meniadakan kredensial statis tertanam (*no hardcoded secrets*), dan melindungi memori flash menggunakan enkripsi perangkat keras.

## Prasyarat

- Memahami arsitektur protokol MQTT dan konfigurasi broker dari [Chapter 14](chapter-14).
- Memahami dasar komunikasi soket TCP/IP terenkripsi dari [Chapter 12](chapter-12).
- Memahami konsep dasar kriptografi asimetris (kunci privat, kunci publik, dan fungsi hash kriptografis SHA-256).

## Konsep dan teori

### 1. Pemodelan Ancaman STRIDE untuk IoT

Kerangka kerja STRIDE memetakan vektor serangan spesifik pada sistem perangkat terhubung:

| Kategori Ancaman | Deskripsi dalam Konteks IoT | Contoh Skenario Serangan | Mitigasi Kriptografis |
| :--- | :--- | :--- | :--- |
| **Spoofing (Pemalsuan Identitas)** | Peretas menyamar sebagai sensor node sah | Mengirim data suhu palsu untuk memicu alarm kebakaran | Otentikasi sertifikat X.509 (mTLS) |
| **Tampering (Manipulasi Data)** | Mengubah muatan data saat melintasi jaringan | Mengubah nilai perintah katup pipa air industri | Enkripsi integritas TLS (AES-GCM/Poly1305) |
| **Repudiation (Penyangkalan)** | Perangkat menyangkal telah mengirimkan perintah | Operator mengklaim tidak mematikan mesin pabrik | Tanda tangan digital (*Digital Signature*) & Audit Log |
| **Information Disclosure (Bocoran Data)** | Menguping transmisi nirkabel (*Eavesdropping*) | Menangkap data lokasi atau kata sandi plaintext | Enkripsi transport TLS v1.3 wajib |
| **Denial of Service (Pikulan Layanan)** | Membanjiri broker dengan paket sampah | Menghabiskan RAM broker sehingga data kritis macet | Pembatasan laju (*Rate Limiting*) & ACL |
| **Elevation of Privilege (Eskalasi Hak)** | Mengambil alih akses konfigurasi admin | Sensor biasa mengirim perintah reboot ke gateway | Matriks otorisasi peran (*RBAC / MQTT ACL*) |

### 2. Identitas Kriptografis & Sertifikat X.509

Sistem keamanan enterprise menolak penggunaan nama pengguna dan kata sandi statis bersama (*shared password*). Setiap perangkat dibekali:
- **Private Key**: Kunci rahasia yang digenerasi di dalam perangkat dan **tidak pernah boleh diekspor** keluar dari memori flash terenkripsi atau modul perangkat keras aman (*Hardware Secure Element* seperti ATECC608A / OPTIGA Trust).
- **Device Certificate (X.509)**: Berkas publik yang memuat nama umum perangkat (*Common Name*, misal `node-env-01`), kunci publik perangkat, masa berlaku (`notBefore` dan `notAfter`), serta ditandatangani secara sah oleh **Root Certificate Authority (CA)** internal lembaga.

Standar panjang kunci modern:
- **ECC (Elliptic Curve Cryptography)**: Minimal kurva **NIST P-256 (secp256r1)** (sangat disukai pada mikrokontroler karena komputasi cepat dan ukuran memori kecil).
- **RSA**: Minimal **2048 bit** (kunci 1024 bit dianggap tidak aman dan ditolak).

### 3. Mutual TLS (mTLS v1.3) Handshake

Pada TLS standar situs web biasa, hanya server yang memiliki sertifikat (otentikasi satu arah). Pada **Mutual TLS (mTLS)**, otentikasi berlangsung dua arah:
1. Mikrokontroler menghubungi broker MQTT port `8883`.
2. Broker mengirimkan sertifikat server; mikrokontroler memverifikasi bahwa sertifikat tersebut ditandatangani oleh Root CA yang terpasang di firmware.
3. Broker meminta sertifikat klien (*CertificateRequest*); mikrokontroler mengirimkan sertifikat X.509 miliknya dan bukti kepemilikan kunci privat melalui paket *CertificateVerify*.
4. Broker memvalidasi sertifikat mikrokontroler terhadap Root CA internal. Jika lolos, kanal terenkripsi terbentuk menggunakan algoritma modern dengan properti *Perfect Forward Secrecy* (PFS).

### 4. Matriks Otorisasi Access Control List (ACL)

Meskipun perangkat telah terhubung lewat mTLS, perangkat tersebut **tidak boleh** diizinkan membaca atau menulis ke sembarang topik MQTT.

Prinsip **Hak Akses Terkecil (*Principle of Least Privilege*)** ditegakkan menggunakan pola ACL ([`mosquitto_acl.conf`](content/chapter-28/src/mosquitto_acl.conf)):
```text
pattern write iot/fleet/%u/telemetry
pattern write iot/fleet/%u/status
pattern read  iot/fleet/%u/cmd/+
```
Di mana variabel `%u` dipetakan otomatis ke identitas *Common Name* sertifikat klien yang terotentikasi.
Konsekuensinya:
- Node `node-env-01` diizinkan menulis ke `iot/fleet/node-env-01/telemetry`.
- Jika `node-env-01` mencoba berlangganan (*subscribe*) ke `iot/fleet/node-env-02/telemetry`, broker langsung memblokir akses (*eavesdropping prevention*).
- Jika `node-env-01` mencoba mengirimkan perintah sabotase ke `iot/fleet/node-env-02/cmd/relay`, broker langsung menolak paket (*spoofing prevention*).

### 5. Panduan Keamanan IoT NIST IR 8259

Publikasi NIST IR 8259 menetapkan lima pilar kapabilitas dasar perangkat IoT:
1. **Device Identification**: Perangkat dapat diidentifikasi secara unik secara logis dan fisik.
2. **Device Configuration**: Konfigurasi keamanan perangkat dapat diubah secara aman dari jarak jauh.
3. **Data Protection**: Seluruh data yang tersimpan di memori (*data at rest*) dan data yang melintasi jaringan (*data in transit*) terlindungi secara kriptografis.
4. **Logical Access to Interfaces**: Seluruh antarmuka fisik (UART, JTAG, USB) dan antarmuka jaringan dibatasi otentikasi ketat.
5. **Software Update**: Firmware dapat diperbarui secara terverifikasi (tanda tangan digital) untuk menambal kerentanan di masa depan.

### 3.1 Landasan Matematis: Kompleksitas Komputasi Kriptografi Elliptic Curve (ECDSA) (Mathematical Foundations)

Keamanan IoT modern mengandalkan kriptografi kurva eliptis (*Elliptic Curve Cryptography* / ECC) seperti kurva NIST P-256 (secp256r1) karena efisiensi panjang kunci yang jauh lebih ringkas dibanding RSA:

1. **Perbandingan Kekuatan Keamanan & Ukuran Kunci**:
   Tingkat keamanan $k$ bit simetris yang setara dirumuskan menurut rekomendasi NIST SP 800-57:
   - RSA-2048 memberikan kekuatan keamanan $\approx 112\text{ bit}$ simetris (panjang kunci publik: 256 byte).
   - RSA-3072 memberikan kekuatan keamanan $\approx 128\text{ bit}$ simetris (panjang kunci publik: 384 byte).
   - ECC P-256 memberikan kekuatan keamanan $\approx 128\text{ bit}$ simetris dengan panjang kunci publik hanya **64 byte** (atau 33 byte terkompresi).

2. **Beban Transmisi Handshake TLS (Worked Example)**:
   Sertifikat digital X.509 berbasis RSA-2048 memiliki ukuran tipikal $L_{\text{cert,RSA}} \approx 1800\text{ byte}$, sedangkan sertifikat ECDSA P-256 hanya $L_{\text{cert,ECC}} \approx 650\text{ byte}$.
   Pada mutual TLS (mTLS v1.3), kedua belah pihak mempertukarkan sertifikat (perangkat $\leftrightarrow$ server). Penghematan byte selama negosiasi handshake adalah:
   $$
   \Delta L_{\text{handshake}} = 2 \times (L_{\text{cert,RSA}} - L_{\text{cert,ECC}}) = 2 \times (1800 - 650) = 2300\text{ byte}
   $$
   Pengurangan lebih dari 2 KiB data transmisi pada setiap proses pembentukan sesi TLS memangkas konsumsi energi radio mikrokontroler hingga $\approx 60\%$, membuktikan keunggulan mutlak cipher-suite ECDSA (seperti `TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256`) untuk sistem tertanam.

## Latihan

1. **Analisis Vektor Serangan**:
   Gunakan kerangka kerja STRIDE untuk menganalisis risiko sistem IoT jika seluruh pembacaan sensor dikirim menggunakan protokol MQTT murni (port `1883`) tanpa TLS melalui jaringan Wi-Fi publik kampus. Sebutkan dua kategori STRIDE yang paling rentan tereksploitasi dan jelaskan dampaknya.
2. **Evaluasi Kekuatan Kunci PKI**:
   Jelaskan mengapa algoritma kurva eliptik **ECC NIST P-256** lebih direkomendasikan untuk mikrokontroler seperti ESP32 dibandingkan algoritma **RSA 2048-bit**, ditinjau dari ukuran payload jabat tangan (*handshake packet size*), kebutuhan RAM, dan konsumsi daya komputasi matematika.
3. **Pemberlakuan Aturan ACL**:
   Jika konfigurasi broker Anda secara tidak sengaja memuat baris:
   ```text
   user anonymous
   topic readwrite #
   ```
   Jelaskan bencana keamanan siber yang dapat terjadi pada seluruh fasilitas gedung pintar Anda, dan bagaimana cara memperbaikinya.

## Tugas

Bangun dan uji sistem evaluasi keamanan siber IoT terintegrasi menggunakan Python:

1. **Modul Evaluator Sertifikat X.509**:
   Implementasikan kelas `X509CertMock` yang memvalidasi masa aktif sertifikat (`not_before` dan `not_after`) serta memastikan panjang kunci memenuhi standar minimal (ECC $\ge 256\text{ bit}$, RSA $\ge 2048\text{ bit}$).
2. **Mesin Penegak Access Control List (ACL)**:
   Bangun kelas `MqttAclEngine` yang mem-parse aturan berbasis pola `%u` dan menguji otorisasi empat skenario akses:
   - Akses tulis telemetri ke topik sendiri (harus diizinkan).
   - Akses baca telemetri milik perangkat lain (harus diblokir).
   - Akses tulis perintah ke topik perangkat lain (harus diblokir).
   - Akses pengawasan admin ke topik wildcard `#` (harus diizinkan).
3. **Analisis Kerentanan STRIDE Otomatis**:
   Implementasikan fungsi `evaluate_stride_security` yang memindai payload telemetri terhadap potensi ketiadaan identitas (*Spoofing*), ketiadaan pelindung urutan (*Tampering*), dan kebocoran kredensial plaintext (*Information Disclosure*).
4. **Konfigurasi ACL Mosquitto**:
   Susun file konfigurasi [`mosquitto_acl.conf`](content/chapter-28/src/mosquitto_acl.conf) yang melarang akses anonim dan mengisolasi topik per perangkat.

### Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Validasi Sertifikat PKI & Kriptografi** | 35% | Evaluator memvalidasi masa berlaku dan kekuatan kunci dengan tepat; sertifikat kedaluwarsa atau kunci lemah ditolak secara konsisten. |
| **Penegakan Matriks Otorisasi MQTT ACL** | 35% | Logika isolasi topik per perangkat berfungsi akurat; akses lintas perangkat (eavesdropping dan spoofing) berhasil diblokir secara tegas. |
| **Pemodelan Ancaman STRIDE & Konfigurasi** | 30% | Pemindai STRIDE mendeteksi celah payload tidak aman; berkas konfigurasi ACL Mosquitto memenuhi kaidah industri dan NIST IR 8259. |

## Ringkasan

1. **Pertahanan Berlapis**: Keamanan IoT menuntut perlindungan simultan pada tingkat identitas fisik, enkripsi transport, dan otorisasi aplikasi.
2. **Otentikasi Kuat**: Penggunaan sertifikat X.509 pada protokol mTLS v1.3 meniadakan ketergantungan pada kata sandi statis yang rentan bocor.
3. **Isolasi Mutlak**: Konfigurasi MQTT ACL berbasis pola `%u` mengisolasi setiap perangkat hanya pada jalurnya sendiri, mengeliminasi risiko peretasan lateral antar perangkat.
4. **Standar Kepatuhan**: Kepatuhan terhadap pedoman NIST IR 8259 menjamin perangkat IoT siap menghadapi ancaman keamanan siber modern.

## Referensi
- NIST Special Publication 800-57 Part 1 Rev. 5, *Recommendation for Key Management*, NIST, 2020.
- IETF RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*, Internet Engineering Task Force.

1. National Institute of Standards and Technology (NIST). *NIST IR 8259: Foundational Cybersecurity Activities for IoT Device Manufacturers*.
2. Rescorla, E. *The Transport Layer Security (TLS) Protocol Version 1.3 (RFC 8446)*. Internet Engineering Task Force (IETF).
3. Eclipse Mosquitto. *Mosquitto Authentication and Topic Access Control List (ACL) Architecture*. https://mosquitto.org/man/mosquitto-conf-5.html
