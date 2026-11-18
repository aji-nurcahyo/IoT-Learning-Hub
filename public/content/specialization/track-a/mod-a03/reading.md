# Modul A03 — Matter Core Protocol, Thread Mesh & Cross-Ecosystem Commissioning

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Membedakan peran node dalam topologi Thread mesh (Leader, Router, Child, Border Router).
2. Menganalisis alur protokol commissioning Matter menggunakan Password-Authenticated Key Exchange (PASE - SPAKE2+).
3. Memverifikasi integritas sertifikat identitas perangkat Device Attestation Certificate (DAC) berbasis rantai PKI X.509.
4. Mengimplementasikan simulasi state-machine commissioning perangkat dan komunikasi kluster On/Off secara lokal.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 28, Chapter 34.
- Modul Jalur Peminatan Prasyarat: Modul A01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Paradigma Standar Terbuka Matter & Thread
Industri otomasi rumah cerdas selama bertahun-tahun terfragmentasi oleh ekosistem tertutup (Apple HomeKit, Google Home, Amazon Alexa, Tuya, SmartThings) yang memaksa pengguna menginstal jembatan (*bridges/gateways*) proprietary multi-vendor.

Standar **Matter** (yang distandarisasi oleh *Connectivity Standards Alliance* / CSA) mengubah paradigma ini dengan menyediakan lapisan aplikasi IP (*Application Layer over IPv6*) terpadu yang dapat berjalan di atas media jaringan heterogen:
- **Thread**: Protokol jaringan mesh berdaya rendah berbasis IEEE 802.15.4 (6LoWPAN) untuk sensor, kunci pintu, dan termostat bertenaga baterai.
- **Wi-Fi / Ethernet**: Untuk perangkat ber-bandwidth tinggi seperti kamera pintar dan TV cerdas.
- **Bluetooth Low Energy (BLE)**: Digunakan murni sebagai kanal *commissioning/onboarding* awal untuk memasukkan perangkat ke dalam jaringan.

### 2. Kriptografi Commissioning: PASE vs CASE
Matter mengeliminasi transmisi kata sandi jaringan dalam teks polos melalui dua tahap pembentukan sesi kriptografis yang sangat aman:
1. **Passcode-Authenticated Session Establishment (PASE)**:
   - Digunakan saat perangkat pertama kali dikeluarkan dari kotak kemasan (*factory-new*).
   - Pengguna memindai kode QR atau memasukkan PIN 8-digit manual yang tertera di bodi perangkat.
   - Protokol mengeksekusi algoritma kriptografi **SPAKE2+** (*Simple Password-Authenticated Key Exchange 2+*), sebuah skema *zero-knowledge proof* yang memungkinkan komisioner dan perangkat menyepakati kunci simetris terenkripsi tanpa pernah mentransmisikan PIN setup melalui udara.
2. **Device Attestation**: Komisioner memverifikasi keaslian perangkat keras melalui rantai sertifikat PKI X.509 (*Device Attestation Certificate* / DAC) yang ditandatangani oleh *Product Attestation Intermediate* (PAI) dan otoritas sertifikasi terakreditasi CSA.
3. **Certificate-Authenticated Session Establishment (CASE)**:
   - Digunakan untuk komunikasi operasional harian di dalam jaringan mesh Thread IPv6.
   - Berbasis sertifikat operasional *Node Operational Certificate* (NOC) yang dikeluarkan oleh Fabric Administrator, menjamin enkripsi *end-to-end* (AES-128-CCM) antar node.

### 3. Fitur Multi-Admin Matter
Salah satu terobosan arsitektural terbesar Matter adalah kemampuan **Multi-Admin**. Satu perangkat lampu atau termostat Thread yang sama dapat dimasukkan (*commissioned*) ke dalam beberapa ekosistem independen sekaligus (misalnya dikendalikan bersamaan dari aplikasi Apple Home, Google Assistant, dan Home Assistant lokal) tanpa bentrok kontrol dan tanpa memerlukan integrasi cloud-to-cloud.

### 4. Landasan Matematis: Pertukaran Kunci SPAKE2+ & Penurunan Kunci Kriptografi

1. **Prinsip Protokol SPAKE2+**:
   SPAKE2+ beroperasi pada kurva eliptik Weierstrass (standar NIST P-256). Kunci setup pengguna $P$ dikonversi menjadi skalar $w_0$ dan titik kurva $L = w_1 cdot P_{	ext{generator}}$:
   - Komisioner mengirimkan titik kurva terblind:
     $$
     X = x cdot P_{	ext{generator}} + w_0 cdot M
     $$
   - Perangkat membalas dengan titik kurva terblind:
     $$
     Y = y cdot P_{	ext{generator}} + w_0 cdot N
     $$
     di mana $M$ dan $N$ adalah titik konstan generator kurva yang telah ditentukan standar.
   - Kunci bersama rahasia dihitung sebagai:
     $$
     K = x cdot (Y - w_0 N) = y cdot (X - w_0 M) = x cdot y cdot P_{	ext{generator}}
     $$
   Pihak ketiga yang menyadap sinyal radio tidak dapat menebak nilai $x$, $y$, maupun $w_0$ berkat ketangguhan masalah logaritma diskrit kurva eliptik (*Elliptic Curve Discrete Logarithm Problem* / ECDLP).

2. **Worked Numerical Example (Alur Commissioning)**:
   - **Kredensial Setup**: Passcode 8-digit = 20202021, Discriminator = 3840 (0x0F00).
   - Komisioner memindai QR payload MT:Y.0123... via BLE.
   - Handshake SPAKE2+ menghasilkan kunci sesi derivasi HKDF 256-bit:
     $$
     K_{	ext{session}} = 	ext{HKDF-Extract}(	ext{Salt}, 	ext{SharedSecret}) implies 	ext{Hash Output}
     $$
   - Transmisi *Thread Operational Dataset* terenkripsi:
     - Network PAN ID = 0x4AF2
     - Channel = 25 (Frekuensi $2475	ext{ MHz}$, aman dari Wi-Fi Ch 6)
     - Network Key 128-bit diinjeksi ke radio IEEE 802.15.4.
   - Perangkat memutus BLE, beralih ke radio 802.15.4, bergabung ke Thread mesh, dan menerima alamat IPv6 Unicast fd00:db8::1.

## Latihan

## Latihan Pemahaman Mandiri

1. **Apa perbedaan mendasar antara pembentukan sesi aman PASE dan CASE pada standar Matter?**
   - *Jawaban*: PASE (*Passcode-Authenticated Session Establishment*) menggunakan passcode setup 8-digit dengan algoritma SPAKE2+ untuk onboarding perangkat baru yang belum terdaftar di jaringan, sedangkan CASE (*Certificate-Authenticated Session Establishment*) menggunakan sertifikat operasional PKI X.509 (*Node Operational Certificate* / NOC) untuk komunikasi terenkripsi antar-node yang sudah tergabung di dalam Fabric jaringan.

2. **Mengapa protokol Thread tidak memerlukan koordinator pusat tunggal yang menjadi single point of failure (seperti pada Zigbee konvensional)?**
   - *Jawaban*: Thread menerapkan arsitektur *self-healing* terdesentralisasi. Jika simpul yang bertindak sebagai *Leader* mengalami kegagalan daya, salah satu simpul *Router* yang aktif akan secara otomatis dipromosikan menjadi Leader baru melalui konsensus internal tanpa merusak topologi jaringan mesh.

## Tugas

## Penugasan Mandiri: Pemodelan Siklus Commissioning Matter & Topologi Thread

Kembangkan simulator Python yang memodelkan transisi status perangkat Matter (dari UNCOMMISSIONED -> PASE -> ATTESTATION -> OPERATIONAL). Simulasikan injeksi perintah kluster On/Off dan verifikasi bahwa penolakan terjadi jika Fabric Index tidak valid.

## Ringkasan
- Modul A03 memberikan pemahaman mendalam dan terapan mengenai Matter Core Protocol, Thread Mesh & Cross-Ecosystem Commissioning pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [matter_thread_commissioning_sim.py](src/matter_thread_commissioning_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Connectivity Standards Alliance (CSA), Matter Core Specification Version 1.2, 2023, [https://csa-iot.org/all-solutions/matter/](https://csa-iot.org/all-solutions/matter/) (diperiksa 2026-11-18).
2. Thread Group, Thread Network Architecture and Specifications, 2022, [https://www.threadgroup.org/support#specifications](https://www.threadgroup.org/support#specifications) (diperiksa 2026-11-18).
