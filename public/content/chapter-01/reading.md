# Chapter 01 — Introduction to the Internet of Things

## Overview

Internet of Things (IoT) bukan sekadar perangkat elektronik yang memiliki modul Wi-Fi atau Bluetooth. Sebuah sistem IoT merupakan keterpaduan antara dunia fisik (*physical world*), perangkat tertanam (*embedded node*), infrastruktur jaringan (*connectivity* dan *gateway*), platform pengolah data (*edge* atau *cloud*), serta aplikasi yang mengubah data mentah menjadi keputusan atau tindakan nyata (*actuation*).

Pada chapter pembuka ini, mahasiswa membangun kerangka berpikir sistem (*systems thinking*): bagaimana besaran fisik seperti suhu atau kelembaban berubah menjadi sinyal listrik, dikemas oleh *Microcontroller* sebagai paket *telemetry*, melewati jaringan yang memiliki keterbatasan *bandwidth* dan keandalan, lalu diproses oleh aplikasi sebelum akhirnya menghasilkan aksi balik ke lingkungan.

## Prasyarat

- Tidak ada chapter prasyarat sebelumnya; chapter ini merupakan titik masuk Level 1.
- Pembelajar disarankan membaca panduan [Getting Started](#/getting-started) untuk memahami opsi lingkungan belajar berbasis simulator maupun *hardware*.
- Pemahaman dasar mengenai komputer, jaringan internet secara umum, dan format data teks terstruktur seperti JSON akan membantu saat menganalisis contoh payload.

## Tujuan pembelajaran

Setelah menyelesaikan modul, slide, dan latihan pada chapter ini, mahasiswa mampu:

1. **Membedakan** perangkat terhubung sederhana, *Embedded System* mandiri, *Cyber-Physical System* (CPS), dan sistem IoT berdasarkan aliran data dua arah serta integrasi jaringan.
2. **Memetakan** peran *Sensor*, *Microcontroller*, *Actuator*, *Gateway*, *Connectivity*, dan *Cloud/Edge Platform* pada suatu *use case* nyata.
3. **Menelusuri** aliran data *end-to-end* (*uplink telemetry* dan *downlink command*) beserta titik kegagalan potensialnya.
4. **Mengevaluasi** empat tantangan utama rekayasa IoT: *scalability*, *security*, *interoperability*, dan *reliability*.

## Konsep dan teori

### 1. Definisi Internet of Things dan Evolusi Internet

Secara teknis, **Internet of Things** merujuk pada jaringan objek fisik ("Things") yang dilengkapi *Sensor*, *Actuator*, pemroses komputasi (*Embedded System*), dan antarmuka komunikasi sehingga mampu mengamati lingkungan, bertukar data secara otomatis melalui protokol jaringan standar, serta berinteraksi dengan sistem perangkat lunak maupun dunia fisik tanpa selalu menunggu input manual manusia.

Evolusi menuju IoT dapat dipahami melalui empat fase utama:

| Fase | Fokus Utama | Karakteristik Aliran Data | Contoh |
| --- | --- | --- | --- |
| **Internet of Documents** | Pertukaran berkas & halaman web | Manusia mengakses server statis | Web awal (HTTP/HTML) |
| **Internet of People** | Komunikasi & media sosial | Konten dibuat dan dikonsumsi manusia | Email, pesan instan, media sosial |
| **Internet of Devices (M2M)** | Koneksi titik-ke-titik antar mesin | Otomasi terisolasi dalam satu vendor | Mesin ATM, telemetry industri tertutup |
| **Internet of Things (IoT)** | Ekosistem terdistribusi & interoperabel | *Telemetry* otomatis + analitik + umpan balik kendali | *Smart agriculture*, *smart grid*, pemantauan BTS |

Perbedaan krusial antara koneksi *Machine-to-Machine* (M2M) klasik dan IoT modern terletak pada **interoperabilitas berbasis standar IP/terbuka** dan **integrasi lintas aplikasi**. Pada IoT, data dari satu simpul sensor tidak terkunci di satu layar lokal; data tersebut dapat dikonsumsi oleh sistem penyimpan deret waktu (*Time-Series Database*), mesin aturan (*rule engine*), hingga sistem analitik prediktif.

### 2. Perbedaan Embedded System, IoT, dan Cyber-Physical Systems (CPS)

Mahasiswa sering menyamakan ketiganya karena sama-sama memakai *Microcontroller* dan berinteraksi dengan perangkat keras. Tabel berikut memperjelas batas konseptual masing-masing:

| Aspek | Embedded System Mandiri | Internet of Things (IoT) | Cyber-Physical System (CPS) |
| --- | --- | --- | --- |
| **Fokus utama** | Menjalankan fungsi spesifik di dalam perangkat | Konektivitas, pengumpulan *telemetry*, layanan terdistribusi | Integrasi ketat komputasi dan dinamika proses fisik |
| **Konektivitas jaringan** | Opsional (sering terisolasi) | Wajib (lokal maupun internet) | Umumnya terhubung, tetapi fokus pada *control loop* |
| **Kendala waktu (*real-time*)** | Tergantung fungsi (bisa *hard real-time*) | Bervariasi; latensi jaringan sering tak terjamin | Ketat (*closed-loop* stabil terhadap dinamika fisik) |
| **Contoh khas** | Pengendali mesin cuci, kalkulator | Node cuaca mengirim data tiap 5 menit ke dashboard | Sistem pengereman ABS, kendali terbang *drone* |

Sebuah perangkat dapat berada di irisan ketiganya. Misalnya, sistem irigasi presisi yang mengukur kelembaban tanah secara *real-time*, mengeksekusi kendali pompa tertutup (*closed-loop*), sekaligus melaporkan status dan menerima jadwal dari server jarak jauh merupakan *Embedded System* yang membentuk CPS dan terhubung dalam arsitektur IoT.

### 3. Komponen Ekosistem IoT

Sebuah ekosistem IoT utuh terdiri atas enam elemen fungsional:

1. **Sensor**: Transduser yang mengubah besaran fisik (suhu, intensitas cahaya, tekanan, kadar gas, getaran) menjadi besaran listrik (tegangan, arus, resistansi, atau sinyal digital I2C/SPI).
2. **Microcontroller / Embedded Node**: Unit komputasi berdaya rendah (misalnya keluarga ESP32) yang menjalankan *Firmware* untuk membaca sensor, memfilter *noise*, memformat pesan, serta mengelola daya dan antarmuka komunikasi.
3. **Actuator**: Komponen keluaran yang mengubah sinyal kendali listrik menjadi aksi fisik (LED indikator, *buzzer*, relay, katup solenoid, motor DC, atau servo).
4. **Connectivity**: Media dan protokol lapis fisik/tautan untuk memindahkan data, baik jarak dekat berdaya rendah (BLE, Zigbee), jaringan lokal berkecepatan menengah (Wi-Fi, Ethernet), jarak jauh berdaya rendah / LPWAN (LoRaWAN, NB-IoT), maupun seluler (4G LTE/5G).
5. **Gateway**: Perangkat perantara yang menjembatani jaringan sensor lokal berdaya rendah (misalnya LoRa atau BLE) menuju jaringan IP/cloud, sekaligus melakukan agregasi, validasi awal, atau *local buffering* ketika koneksi internet terputus.
6. **Platform & Application**: Lapisan perangkat lunak (seperti *MQTT Broker*, basis data deret waktu, *dashboard* pemantauan, sistem peringatan, atau modul analitik) tempat manusia maupun sistem otomasi mengambil keputusan.

### 4. Alur Data End-to-End (Uplink & Downlink)

Gambar berikut mengilustrasikan pemisahan tanggung jawab sepanjang perjalanan data dari dunia fisik ke aplikasi dan kembali ke *Actuator*:

![Diagram alur data end-to-end sistem IoT dari sensor hingga aplikasi dan actuator](content/chapter-01/diagram.svg)

Perhatikan dua arah aliran pada diagram tersebut:

- **Uplink (Telemetry Path)**: Dunia fisik $\rightarrow$ Sensor $\rightarrow$ Embedded Node (sampling & enkapsulasi) $\rightarrow$ Gateway/Network $\rightarrow$ Platform (ingest & validasi) $\rightarrow$ Application (visualisasi & logika).
- **Downlink (Command / Control Path)**: Application (keputusan otomatis atau input operator) $\rightarrow$ Platform/Broker $\rightarrow$ Gateway $\rightarrow$ Embedded Node $\rightarrow$ Actuator (aksi fisik).

Pada sistem yang dirancang baik, komunikasi antar-lapisan memakai format payload terstruktur dan ringan (misalnya JSON untuk kejelasan atau format biner seperti CBOR/Protobuf untuk efisiensi *bandwidth*). Contoh payload *telemetry* **sintetis** (bukan pembacaan hardware):

```json
{
  "device_id": "gh-node-01",
  "seq": 3,
  "temp_c": 30.6,
  "humidity_pct": 61.0,
  "source": "synthetic"
}
```

Menyertakan `seq` (*sequence number*), identitas perangkat (`device_id`), satuan eksplisit pada nama field (`temp_c`, `humidity_pct`), serta penanda sumber (`source`) mencegah kebingungan saat menganalisis ribuan paket di sisi server.

### 5. Analisis Beban Data Sederhana (Mathematical Foundation)

Sebelum memilih jaringan komunikasi, insinyur IoT perlu memperkirakan volume data harian. Jika sebuah node mengirim payload berukuran $B$ byte setiap interval waktu $\Delta t$ detik sepanjang hari (86.400 detik), maka jumlah paket harian $N_{\text{hari}}$ dan total volume data mentah aplikasi $V_{\text{hari}}$ adalah:

$$
N_{\text{hari}} = \frac{86400}{\Delta t}, \qquad V_{\text{hari}} = N_{\text{hari}} \times B \text{ (byte/hari)}
$$

Laju data rata-rata (*average application bit rate*) $R_{\text{avg}}$ dalam bit per detik (bps) adalah:

$$
R_{\text{avg}} = \frac{B \times 8}{\Delta t}
$$

Perhitungan ini baru mencakup ukuran *payload* aplikasi; pada jaringan nyata masih terdapat *header overhead* dari protokol transport (TCP/UDP), IP, dan lapisan MAC/radio serta paket ulang akibat *packet loss*.

### 6. Contoh Terapan (Worked Example)

**Kasus**: Sebuah stasiun pemantau rumah kaca (*smart greenhouse*) memiliki 25 node sensor suhu dan kelembaban. Setiap node mengirim payload JSON sebesar $B = 110\text{ byte}$ setiap $\Delta t = 60\text{ detik}$ melalui *Gateway* lokal. Hitung jumlah paket harian dan volume payload aplikasi total yang diterima *Gateway*!

**Penyelesaian**:
1. Jumlah paket per node per hari:
   $$N_{\text{node}} = \frac{86400}{60} = 1440\text{ paket/hari}$$
2. Volume payload per node per hari:
   $$V_{\text{node}} = 1440 \times 110\text{ byte} = 158.400\text{ byte} \approx 154{,}7\text{ KiB/hari}$$
3. Untuk 25 node sekaligus:
   $$N_{\text{total}} = 25 \times 1440 = 36.000\text{ paket/hari}$$
   $$V_{\text{total}} = 25 \times 158.400\text{ byte} = 3.960.000\text{ byte} \approx 3{,}78\text{ MiB/hari}$$
4. Laju data rata-rata total aplikasi:
   $$R_{\text{total}} = \frac{25 \times 110 \times 8}{60} \approx 366{,}7\text{ bps}$$

**Analisis Engineering**: Beban *bandwidth* rata-rata di bawah 1 kbps tampak sangat kecil, tetapi apabila 25 node mengirimkan data tepat pada detik yang sama (sinkron), terjadi lonjakan tumbukan (*collision*) di kanal nirkabel. Selain itu, jika interval dipercepat menjadi $\Delta t = 1\text{ detik}$ tanpa agregasi di *Edge*, jumlah paket melonjak 60 kali lipat menjadi 2,16 juta paket per hari—yang langsung berdampak pada konsumsi baterai dan kuota penulisan basis data.

### 7. Implementasi Praktis (Path A: Simulasi Pipeline Software)

Karena Chapter 01 berfokus pada fondasi alur data sebelum masuk ke *wiring* elektronika dan pemrograman *Microcontroller*, praktik chapter ini menggunakan **Path A (Software Simulation)** dengan skrip Python standar [`iot_flow_demo.py`](content/chapter-01/src/iot_flow_demo.py) dan dataset sintetis [`telemetry.csv`](content/chapter-01/telemetry.csv).

Skrip memodelkan tiga tanggung jawab utama sistem IoT:
1. Membaca paket *telemetry* terstruktur (`device_id`, `seq`, `temp_c`, `humidity_pct`, `source`).
2. Menjalankan **validasi batas fisik di Gateway** (menolak `temp_c = 125.0` yang berada di luar rentang wajar sensor $-40\dots 85\,^\circ\text{C}$ agar data rusak tidak meracuni basis data atau memicu *Actuator* secara keliru).
3. Menerbitkan keputusan *downlink* (`FAN_ON` jika `temp_c >= 30.0`, selain itu `FAN_OFF`).

Cara menjalankan simulasi:

```sh
python public/content/chapter-01/src/iot_flow_demo.py
```

Hasil eksekusi nyata pada Python 3.12.10 terekam lengkap di berkas bukti [outputs.md](content/chapter-01/outputs.md): dari 6 baris data sintetis, 5 paket valid diteruskan ke platform dan 1 paket anomali ditolak oleh *Gateway*.

### 8. Tantangan Utama Sistem IoT & Kesalahan Umum

Empat tantangan yang harus dipertimbangkan sejak tahap desain awal:

1. **Scalability**: Sistem yang bekerja lancar untuk 2 perangkat di meja laboratorium sering gagal saat diskalakan ke 500 perangkat di lapangan akibat konflik alamat, kehabisan koneksi broker, atau kemacetan kanal radio.
2. **Security**: Mengacu pada panduan NIST Cybersecurity for IoT (*NISTIR 8259*), perangkat IoT sering memiliki sumber daya terbatas namun terhubung terus-menerus. Kesalahan fatal yang sering terjadi adalah menanam *hardcoded password* di *Firmware*, memakai komunikasi teks polos (*plaintext*) pada jaringan terbuka, atau membiarkan port konfigurasi tanpa autentikasi.
3. **Interoperability**: Perangkat dari produsen berbeda sering menggunakan format payload, satuan, atau protokol yang tidak seragam. Pemisahan skema data dan protokol standar (misalnya MQTT/HTTP + JSON terstandar) memudahkan integrasi lintas sistem.
4. **Reliability**: Dunia nyata penuh gangguan—putus listrik, sinyal RF melemah, sensor terlepas, atau paket hilang. Sistem andal merancang mekanisme *timeout*, *watchdog*, penanda urutan (`seq`), dan kondisi aman (*fail-safe*) ketika komunikasi terputus.

**Kesalahan Umum Pemula & Troubleshooting Konseptual**:

| Kesalahan Umum | Dampak di Sistem Nyata | Perbaikan Desain |
| --- | --- | --- |
| Menganggap perangkat terhubung Wi-Fi sudah otomatis "sistem IoT lengkap" | Tidak ada validasi data, tidak ada pemantauan status putus (*offline*), sulit dirawat | Definisikan batas *Edge/Gateway*, *heartbeat*, dan skema payload sejak awal |
| Mengirim data mentah tanpa satuan dan *sequence number* | Data membingungkan saat *debugging*, paket hilang tidak terdeteksi | Wajib sertakan unit (`temp_c`), `seq`, dan identitas sumber |
| Mengandalkan koneksi internet selalu aktif untuk keselamatan | Saat internet putus, pompa/pemanas tetap menyala tanpa kendali | Tempatkan *safety threshold* dan *fail-safe* di level lokal (*Embedded Node/Edge*) |

### 9. Aplikasi di Dunia Nyata

- **Telecommunications & Wireless Infrastructure**: Pemantauan suhu ruang kabinet *Base Transceiver Station* (BTS), tegangan baterai cadangan, dan status pintu akses menara telekomunikasi di daerah terpencil menggunakan koneksi seluler/LPWAN untuk mencegah *downtime* jaringan.
- **Smart Agriculture**: Pemantauan kelembaban tanah, suhu udara mikro, dan konduktivitas nutrisi pada rumah kaca atau lahan perkebunan, terhubung dengan katup irigasi otomatis berbasis ambang batas.
- **Smart Home & Building Energy**: Pengukuran konsumsi daya listrik per zona, deteksi kebocoran air, dan kontrol pencahayaan atau HVAC adaptif berdasarkan okupansi ruangan.
- **Environmental Monitoring & Industry**: Pemantauan kualitas udara perkotaan ($PM_{2.5}$, $CO_2$), tinggi muka air sungai untuk peringatan dini banjir, serta pemantauan getaran motor industri (*predictive maintenance*).

## Latihan

Latihan lengkap tersedia pada modul [Exercises](content/chapter-01/exercises.md) (dapat dibuka langsung melalui tab **Exercises** atau diunduh). Ringkasan cakupan latihan:

1. **Konseptual**: Membandingkan perangkat *embedded* mandiri, CPS, dan sistem IoT pada studi kasus lampu lalu lintas pintar dan monitor detak jantung portabel.
2. **Analisis Alur Data**: Mengidentifikasi komponen *Sensor*, *Microcontroller*, *Gateway*, *Platform*, dan *Actuator* beserta arah *uplink/downlink* pada sistem pemantau menara BTS.
3. **Perhitungan Rekayasa**: Menghitung beban data harian untuk skenario 100 node sensor lingkungan dengan variasi interval sampling.
4. **Mini Challenge & Simulasi**: Memodifikasi aturan validasi pada `iot_flow_demo.py` agar mendeteksi lonjakan suhu tidak realistis antar-paket berurutan (*rate-of-change check*).

## Tugas

Rancang dokumen pemetaan arsitektur konseptual **Sistem Monitoring & Peringatan Dini Lingkungan** untuk salah satu konteks berikut: (a) ruang server/kabinet BTS telekomunikasi, (b) lahan *smart agriculture*, atau (c) pemantauan tinggi muka air sungai. Petunjuk lengkap, format artefak, dan daftar periksa verifikasi tersedia pada halaman **Tugas & Rubrik** ([assignment.md](content/chapter-01/assignment.md)).

Ringkasan distribusi **Rubrik Penilaian (Total 100 Poin)**:

| Kriteria | Poin | Indikator Penilaian Utama |
| --- | --- | --- |
| Pemetaan komponen ekosistem | 25 | Ketepatan membedakan sensor, MCU, gateway, konektivitas, platform, dan actuator |
| Analisis alur data uplink & downlink | 25 | Kejelasan skema payload (satuan, `seq`), alur validasi, dan mekanisme umpan balik |
| Estimasi beban data & batasan teknis | 25 | Ketepatan perhitungan paket/volume harian serta identifikasi mode kegagalan |
| Kejelasan diagram, keselamatan & referensi | 25 | Keterbacaan diagram blok, kesadaran keamanan/fail-safe, dan rujukan primer |

## Ringkasan

- Sistem IoT menyatukan **penginderaan fisik**, **pemrosesan tertanam**, **jaringan & gateway**, **platform data**, dan **aplikasi/aktuasi** dalam satu aliran dua arah (*uplink telemetry* dan *downlink command*).
- Perbedaan utama IoT dibanding *Embedded System* terisolasi terletak pada pertukaran data terstandar melalui jaringan dan kemampuan integrasi lintas layanan, sedangkan CPS menekankan keterikatan *closed-loop* yang ketat terhadap dinamika fisik.
- Simulasi perangkat lunak (`iot_flow_demo.py`) telah diverifikasi pada Python 3.12.10 menggunakan data sintetis untuk memvalidasi penyaringan paket anomali di sisi *Gateway*; chapter ini tidak melibatkan *hardware* fisik sehingga belum menguji latensi jaringan maupun karakteristik listrik nyata.

## Referensi

1. National Institute of Standards and Technology (NIST), *NIST Cybersecurity for IoT Program (NISTIR 8259 Series)*, [https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program](https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program) (diperiksa 2026-11-10).
2. Espressif Systems, *ESP-IDF Programming Guide (ESP32 Overview)*, [https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html) (diperiksa 2026-11-10).
3. OASIS Standard, *MQTT Version 5.0 Specification Overview*, [https://mqtt.org/mqtt-specification/](https://mqtt.org/mqtt-specification/) (diperiksa 2026-11-10).
4. Arduino Official Documentation, *Arduino IDE & Ecosystem Documentation*, [https://docs.arduino.cc/software/ide/](https://docs.arduino.cc/software/ide/) (diperiksa 2026-11-10).

