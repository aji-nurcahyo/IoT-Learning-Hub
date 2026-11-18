# Specialization Master Curriculum (30 Modul)
## IoT Learning Hub — Phase 6A: Curriculum Architecture & Syllabus Specification

Dokumen ini memuat rancangan kurikulum master dan arsitektur akademik untuk 5 Jalur Peminatan (*Specialization Tracks*) dengan total 30 modul pembelajaran tingkat lanjut pada **Internet of Things Learning Hub**.

- **Proyek**: Internet of Things Learning Hub (*From Connected Devices to Intelligent Systems*)
- **Pengembang & Kurator**: Aji Pamungkas Tri Nurcahyo (Institut Teknologi Sumatera - ITERA)
- **Repositori**: `https://github.com/aji-nurcahyo/IoT-Learning-Hub.git`
- **Kebijakan Anti-Slop**: Permanent Active (Mode: **DURING**)
- **Fase**: Phase 6A — Specialization Architecture & Curriculum Design
- **Tanggal Rilis Dokumen**: 18 November 2026

---

## 1. Kerangka Desain & Taksonomi Kedalaman Akademik

Kurikulum peminatan dirancang tidak sebagai pengganti (*replacement*), melainkan sebagai pengayaan lanjutan (*advanced specialization*) di atas fondasi 40 bab kurikulum inti (*Core Curriculum*). Setiap modul diklasifikasikan ke dalam salah satu dari tiga tingkatan kedalaman akademik:

| Tingkat Kedalaman | Definisi & Beban Kognitif | Target Capaian Mahasiswa |
|---|---|---|
| **L2: Undergraduate Complete** | Penguasaan komprehensif tingkat sarjana; integrasi multi-protokol, instrumentasi industri terapan, dan verifikasi laboratorium terstruktur. | Mampu merancang, memprogram, mengkalibrasi, dan memvalidasi subsistem perangkat keras & protokol sesuai standar teknik. |
| **L3: Advanced Engineering** | Rekayasa sistem tingkat lanjut; optimalisasi trade-off kinerja, kuantisasi model matematika, analisis keandalan numerik, dan mitigasi kegagalan kritis. | Mampu menganalisis batas batas fisik/protokol, memodelkan perilaku dinamik sistem, dan merekayasa solusi deterministik berkinerja tinggi. |
| **L4: Research Preparation** | Persiapan riset mutakhir & perancangan state-of-the-art; pemodelan diferensial, fusi sensor multimodal, estimasi keadaan optimal, dan arsitektur terdistribusi skala kota. | Mampu memformulasi hipotesis eksperimental, mengevaluasi metrik ilmiah kuantitatif, dan mempublikasikan artefak riset reproducible. |

---

## 2. Track A — Smart Home & Building Automation

**Target Kompetensi Track**: Memahami, merancang, memodelkan, dan mengevaluasi sistem otomasi bangunan (*Building Management Systems* / BMS) yang interoperabel lintas vendor, beroperasi secara lokal (*local-first resilience*), hemat energi, serta menjamin privasi dan keselamatan penghuni.

### Modul A01: Smart Building Architecture, Zoning & Multi-Protocol Coexistence
- **Kode & Judul**: `A01 — Smart Building Architecture, Zoning & Multi-Protocol Coexistence`
- **Kedalaman Akademik**: **L2: Undergraduate Complete**
- **Prasyarat Kurikulum Inti**: Chapter 01 (IoT Intro), Chapter 02 (Architecture), Chapter 11 (Networking).
- **Ruang Lingkup & Batasan**: Pemodelan hierarki ruang bangunan (Room $\to$ Zone $\to$ Floor $\to$ Facility), koeksistensi spektrum nirkabel $2{,}4\text{ GHz}$ (Wi-Fi 802.11ax, Thread/Zigbee 802.15.4, dan BLE), serta isolasi VLAN jaringan otomasi vs jaringan publik. Tidak membahas instalasi tegangan tinggi AC $220\text{ V}$.
- **Capaian Pembelajaran (LO)**:
  1. Mahasiswa mampu menyusun topologi zonasi logis dan fisik bangunan komersial.
  2. Mahasiswa mampu menganalisis interferensi kanal silang nirkabel antara kanal Wi-Fi (1, 6, 11) dan kanal 802.15.4 (11 hingga 26).
- **Topik Teori Utama**: Arsitektur ANSI/ASHRAE/IES Standard 135 (BACnet over IP), koeksistensi pita $2{,}4\text{ GHz}$, segmentasi jaringan 802.1Q VLAN, dan kedaulatan kendali lokal (*Local Survivability*).
- **Landasan Matematis (KaTeX)**:
  - Model interferensi overlapping channel Carrier-to-Interference Ratio:
    $$
    \text{CIR}_{\text{dB}} = P_{\text{desired}} - 10 \log_{10} \left( \sum_{k=1}^{M} 10^{P_{\text{int},k}/10} \right)
    $$
- **Worked Numerical Example**: Perhitungan margin interferensi kanal 802.15.4 (Kanal 15, frekuensi tengah 2425 MHz) di dekat pemancar Wi-Fi Kanal 6 (bandwidth 20 MHz, 2437 MHz) dengan atenuasi spektrum luar-pita $-35\text{ dB}$.
- **Eksperimen Komputasi**: Skrip simulasi pemetaan spektrum dan pemilihan kanal nirkabel optimal (*clean channel allocation*).
- **Perangkat Lunak & Kebutuhan Hardware**: Wireshark, Python 3.12, simulator jaringan nirkabel. Hardware opsional: ESP32-C3 / nRF52840 dongle.
- **Deliverables & Asesmen**: Laporan alokasi kanal frekuensi dan diagram zonasi VLAN gedung 3 lantai (Rubrik 100 poin).
- **Rujukan Primer**: IEEE Std 802.15.4-2020; ANSI/ASHRAE Standard 135-2020.
- **Koneksi Lanjutan**: Fondasi untuk penempatan sensor okupansi pada Modul A02.
- **Peluang Ekstensi Riset**: Optimasi alokasi frekuensi dinamis berbasis reinforcement learning pada lingkungan RF padat.

### Modul A02: Occupancy Sensing, Environmental Conditioning & Indoor Air Quality (IAQ)
- **Kode & Judul**: `A02 — Occupancy Sensing, Environmental Conditioning & Indoor Air Quality (IAQ)`
- **Kedalaman Akademik**: **L2: Undergraduate Complete**
- **Prasyarat Kurikulum Inti**: Chapter 07 (Analog Sensors & ADC), Chapter 08 (I2C/SPI), Chapter 23 (Edge Processing).
- **Ruang Lingkup & Batasan**: Instrumentasi sensor PIR, radar gelombang milimeter (mmWave 24 GHz / 60 GHz micro-motion), sensor $\text{CO}_2$ NDIR, partikulat $\text{PM}_{2.5}$, dan TVOC. Batasan: pengolahan sinyal baseband mentah radar dicakup pada Track D; A02 fokus pada interpretasi state kehadiran dan pengendalian sirkulasi HVAC.
- **Capaian Pembelajaran (LO)**:
  1. Mengintegrasikan sensor NDIR $\text{CO}_2$ dan radar mmWave untuk mendeteksi okupansi statis vs dinamis.
  2. Menerapkan kontrol deadband dan histeresis pada katup ventilasi udara segar mekanis.
- **Topik Teori Utama**: Prinsip Beer-Lambert pada optik NDIR, ambang batas IAQ ASHRAE 62.1, sensor fusi kehadiran biner (PIR + mmWave), dan kontrol demand-controlled ventilation (DCV).
- **Landasan Matematis (KaTeX)**:
  - Hukum Beer-Lambert serapan radiasi inframerah:
    $$
    I = I_0 \cdot e^{-\alpha \cdot C \cdot L} \implies C = -\frac{1}{\alpha L} \ln\left( \frac{I}{I_0} \right)
    $$
- **Worked Numerical Example**: Kalibrasi konsentrasi $\text{CO}_2$ dari rasio transmisi intensitas optik sensor NDIR berpanjang lintasan optik $L = 5\text{ cm}$ dengan koefisien serapan $\alpha = 0{,}045\text{ ppm}^{-1}\text{cm}^{-1}$.
- **Eksperimen Komputasi**: Pemodelan estimasi laju pertukaran udara ruangan (*Air Changes per Hour* / ACH) dan algoritma pemfilteran state transisi kehadiran tanpa false-trigger.
- **Deliverables & Asesmen**: Modul kontrol logika ventilasi udara otomatis berbasis data IAQ riil/sintetis.
- **Rujukan Primer**: ASHRAE Standard 62.1-2022; ISO 16000-26 (Indoor Air Pollution Sampling).

### Modul A03: Matter Core Protocol, Thread Mesh & Cross-Ecosystem Commissioning
- **Kode & Judul**: `A03 — Matter Core Protocol, Thread Mesh & Cross-Ecosystem Commissioning`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 28 (Security & TLS), Chapter 34 (Matter & Thread).
- **Ruang Lingkup & Batasan**: Implementasi protokol pertukaran kunci PASE (*Password-Authenticated Session Establishment*) dan CASE (*Certificate-Authenticated Session Establishment*), struktur Matter Data Model (Endpoint, Cluster, Attribute, Command), dan Border Router routing IPv6. Tidak membahas pembuatan sertifikat vendor komersial DAC (*Device Attestation Certificate*) resmi dari CA global.
- **Capaian Pembelajaran (LO)**:
  1. Menganalisis alur kriptografi commissioning Matter menggunakan algoritma SPAKE2+.
  2. Mengimplementasikan cluster Matter On/Off dan Level Control pada node virtual/perangkat embedded.
- **Topik Teori Utama**: Protokol kriptografi SPAKE2+, model X.509 Device Attestation, arsitektur Thread Border Router, dan interoperabilitas multi-admin Matter (Apple Home, Google Home, Home Assistant).
- **Landasan Matematis (KaTeX)**:
  - Komputasi pertukaran titik kunci terotentikasi SPAKE2+ pada kurva eliptis:
    $$
    X = xG + wM, \qquad Y = yG + wN
    $$
    $$
    K = x(Y - wN) = y(X - wM) = xyG
    $$
- **Worked Numerical Example**: Verifikasi integritas komputasi kunci sesi bersama $K$ dari koordinat titik kurva terotentikasi tanpa membocorkan PIN setup.
- **Eksperimen Komputasi**: Harness uji emulasi commissioning node Matter dan transmisi perintah kontrol cluster عبر IPv6 Thread mesh.
- **Deliverables & Asesmen**: Log jejak paket interaksi Matter CASE session establishment dan audit payload TLV (*Type-Length-Value*).
- **Rujukan Primer**: Connectivity Standards Alliance (CSA), *Matter Specification v1.3*; Thread Group, *Thread 1.3.0 Specification*.

### Modul A04: Building Energy Optimization, Peak-Shaving & Sub-Metering
- **Kode & Judul**: `A04 — Building Energy Optimization, Peak-Shaving & Sub-Metering`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 09 (Actuators & Control), Chapter 25 (Time-Series DB), Chapter 26 (Dashboards).
- **Ruang Lingkup & Batasan**: Pengukuran daya listrik 3-fasa menggunakan Current Transformer (CT), kalkulasi faktor daya ($\cos \phi$), energi aktif/reaktif/semu, dan algoritma penjadwalan pemutusan beban non-kritis (*load shedding*) untuk menghindari denda penalti lonjakan daya semu (kVA).
- **Capaian Pembelajaran (LO)**:
  1. Menghitung profil daya real, reaktif, dan distorsi harmonik total (THD) dari sinyal arus terdiskritisasi.
  2. Merancang algoritma optimasi pemangkasan beban puncak (*peak shaving*) berbasis ambang batas kapasitas trafo.
- **Topik Teori Utama**: Segitiga daya AC ($P, Q, S$), sampling diskrit True RMS, integrasi sub-metering MODBUS/BACnet, dan strategi pengendalian beban fleksibel.
- **Landasan Matematis (KaTeX)**:
  - Perhitungan daya aktif dan faktor daya dari sampling diskrit $N$ titik:
    $$
    P = \frac{1}{N} \sum_{i=1}^{N} v_i \cdot i_i, \qquad S = V_{\text{RMS}} \cdot I_{\text{RMS}}, \qquad \text{PF} = \frac{P}{S}
    $$
- **Worked Numerical Example**: Evaluasi denda faktor daya jika beban pendingin gedung menyerap $P = 45\text{ kW}$ dengan $Q = 35\text{ kVAR}$ ($\text{PF} = 0{,}789$), serta penentuan kapasitas bank kapasitor kompensasi untuk menaikkan $\text{PF}$ ke $0{,}95$.
- **Eksperimen Komputasi**: Simulasi algoritma *Demand Response* otomatis yang mematikan kompresor pendingin sekunder saat proyeksi beban melebihi daya kontrak.
- **Deliverables & Asesmen**: Model simulasi Python pengendali beban puncak dan dashboard deret waktu konsumsi energi per lantai.
- **Rujukan Primer**: IEC 62053-21 (Electricity Metering Equipment); IEEE Std 1459-2010.

### Modul A05: Life-Safety Integration, Fail-Safe Interlocks & Emergency Evacuation Routing
- **Kode & Judul**: `A05 — Life-Safety Integration, Fail-Safe Interlocks & Emergency Evacuation Routing`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 28 (Security & ACL), Chapter 38 (Fault Injection & Chaos Testing).
- **Ruang Lingkup & Batasan**: Interlock keselamatan fisik antara sistem alarm kebakaran gedung (Fire Alarm System / FAS) dan otomasi ventilasi/pintu darurat. Prinsip fail-secure vs fail-safe. Batasan: sistem ini adalah integrasi pemantauan; sistem pemadam api utama tetap wajib memenuhi sertifikasi perangkat keras independen NFPA 72.
- **Capaian Pembelajaran (LO)**:
  1. Merancang arsitektur interlock perangkat keras dan logika relay fail-safe yang tidak bergantung pada koneksi cloud.
  2. Menganalisis waktu propagasi sinyal evakuasi dan kegagalan cascade subsistem kelistrikan.
- **Topik Teori Utama**: Standar keselamatan jiwa NFPA 101/72, arsitektur relay kontak kering (*Dry Contact*) terawasi (*Supervised Loop* dengan resistor EOL), dan algoritma penentuan jalur evakuasi dinamis bebas asap.
- **Landasan Matematis (KaTeX)**:
  - Model loop deteksi resistansi ujung saluran (End-of-Line / EOL):
    $$
    V_{\text{sense}} = V_{\text{loop}} \cdot \frac{R_{\text{sense}}}{R_{\text{sense}} + R_{\text{wire}} + R_{\text{EOL}}}
    $$
    Diferensiasi kondisi: Terbuka ($V \approx 0$), Normal ($V_{\text{nom}}$), Terpicu Alarm ($R_{\text{EOL}}$ diparalel/dihubung singkat $\to V_{\text{alarm}}$).
- **Worked Numerical Example**: Toleransi tegangan loop pemantau kabel 2 kawat sepanjang 200 meter dengan hambatan loop $18\,\Omega$ dan resistor EOL $4{,}7\text{ k}\Omega$ pada tegangan suplai 24 VDC.
- **Eksperimen Komputasi**: Uji injeksi kesalahan (*fault injection*) pemutusan kabel komunikasi dan pembuktian aktivasi relay pintu darurat otomatis (*unlocked on power loss*).
- **Deliverables & Asesmen**: Diagram skematik loop pemantau terawasi dan skrip uji keandalan logika interlock darurat.
- **Rujukan Primer**: NFPA 72 (National Fire Alarm and Signaling Code); UL 864 (Control Units for Fire-Protective Signaling Systems).

### Modul A06: Capstone — Autonomous Micro-Climate & Demand-Response Building Controller
- **Kode & Judul**: `A06 — Capstone: Autonomous Micro-Climate & Demand-Response Building Controller`
- **Kedalaman Akademik**: **L4: Research Preparation**
- **Prasyarat Kurikulum Inti**: Seluruh modul A01–A05, Chapter 30, Chapter 40.
- **Spesifikasi & Rincian**: Dijabarkan secara mendalam pada Seksi 7 (Capstone Design).

---

## 3. Track B — Industrial IoT & Predictive Maintenance

**Target Kompetensi Track**: Mengembangkan sistem pemantauan kondisi peralatan industri (*Condition-Based Monitoring* / CBM) dan pemeliharaan prediktif (*Predictive Maintenance* / PdM) berbasis instrumentasi getaran presisi tinggi, protokol industri deterministik (Modbus RTU/TCP, OPC UA), pemrosesan sinyal digital domain waktu & frekuensi, serta kepatuhan standar keselamatan fungsional IEC 61508.

### Modul B01: Industrial Automation Architecture, Purdue Model & OT/IT DMZ Security
- **Kode & Judul**: `B01 — Industrial Automation Architecture, Purdue Model & OT/IT DMZ Security`
- **Kedalaman Akademik**: **L2: Undergraduate Complete**
- **Prasyarat Kurikulum Inti**: Chapter 01, Chapter 11, Chapter 28 (Security).
- **Ruang Lingkup & Batasan**: Pemetaan arsitektur otomasi industri mengacu pada model referensi Purdue / ISA-95 (Level 0 Field Device hingga Level 4 Enterprise). Perancangan zona demiliterisasi (Industrial DMZ / IDMZ) dan inspeksi mendalam paket protokol industri. Batasan: konfigurasi fisik firewall perangkat keras proprietary vendor disimulasikan melalui perangkat lunak perutean Linux/iptables.
- **Capaian Pembelajaran (LO)**:
  1. Memetakan aliran data telemetri dan kendali melintasi level-level model Purdue tanpa melanggar batasan segmentasi keselamatan.
  2. Merancang aturan firewall dan proksi data di Industrial DMZ yang mengisolasi jaringan kendali SCADA dari ancaman internet eksternal.
- **Topik Teori Utama**: Model referensi ISA-95/Purdue Enterprise Reference Architecture (PERA), standar keamanan siber industri IEC 62443, konsep *Conduits & Zones*, dan isolasi data dioperasikan melalui *Unidirectional Security Gateways* (Data Diodes).
- **Landasan Matematis (KaTeX)**:
  - Kuantifikasi metrik ketersediaan zona berantai industri:
    $$
    A_{\text{zone}} = \prod_{i=1}^{k} A_{\text{layer}, i}
    $$
- **Worked Numerical Example**: Penentuan waktu rata-rata antar kegagalan (*Mean Time Between Failures* / MTBF) gabungan dari jalur komunikasi 4-tier (Sensor $\to$ PLC $\to$ Scada Gateway $\to$ Cloud Historian).
- **Eksperimen Komputasi**: Pembangunan topologi jaringan tervirtualisasi menggunakan kontainer Docker untuk memverifikasi isolasi Level 2 OT dari akses langsung Level 4 Enterprise.
- **Deliverables & Asesmen**: Laporan arsitektur segmentasi jaringan pabrik dan skrip verifikasi penolakan paket traversal liar.
- **Rujukan Primer**: IEC 62443-3-3 (Security for industrial automation and control systems); ISA-95 Standard Part 1.

### Modul B02: High-Frequency Vibration, Acoustic Emission & Sensor Installation Physics
- **Kode & Judul**: `B02 — High-Frequency Vibration, Acoustic Emission & Sensor Installation Physics`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 07 (ADC), Chapter 08 (SPI), Chapter 35 (Edge AI).
- **Ruang Lingkup & Batasan**: Fisika transduser getaran piezoelektrik (IEPE/ICP), efek pemasangan mekanis (baut stud, magnetik, lilin perekat) terhadap frekuensi resonansi alami sensor, dan fenomena emisi akustik ultrasonik (20 kHz–100 kHz) untuk deteksi keretakan mikro dini.
- **Capaian Pembelajaran (LO)**:
  1. Menghitung pengaruh metode pemasangan sensor terhadap batas frekuensi pengukuran linear getaran mekanis.
  2. Menganalisis respon frekuensi transduser akselerometer industri dan merancang rangkaian penyaring anti-aliasing hardware.
- **Topik Teori Utama**: Karakteristik transduser piezoelektrik, respons sistem mekanis massa-pegas orde-2, resonansi kontak pemasangan, dan standar getaran mesin ISO 10816 / ISO 20816.
- **Landasan Matematis (KaTeX)**:
  - Frekuensi resonansi alami sistem pemasangan sensor getaran:
    $$
    f_n = \frac{1}{2\pi} \sqrt{\frac{k_{\text{mount}}}{m_{\text{sensor}}}}
    $$
    Batas frekuensi linear ($\pm 5\%$ akurasi): $f_{\text{usable}} \le 0{,}2 \cdot f_n$.
- **Worked Numerical Example**: Akselerometer bermassa $m = 35\text{ gram}$ dipasang menggunakan dudukan magnetik berkekakuan kontak $k_{\text{mount}} = 1{,}2 \times 10^7\text{ N/m}$. Hitung frekuensi resonansi $f_n$ dan tentukan batas frekuensi maksimum yang valid untuk pemantauan gearbox!
- **Eksperimen Komputasi**: Simulasi distorsi amplitudo sinyal getaran harmonik saat frekuensi mendekati resonansi dudukan sensor.
- **Deliverables & Asesmen**: Lembar analisis pemilihan metode *mounting* sensor untuk motor induksi 3000 RPM.
- **Rujukan Primer**: ISO 20816-1:2016 (Mechanical vibration — Measurement and evaluation of machine vibration); Norton, H. N., *Handbook of Transducers*.

### Modul B03: Industrial Fieldbus Engineering: Modbus RTU/TCP, OPC UA Information Models & TSN
- **Kode & Judul**: `B03 — Industrial Fieldbus Engineering: Modbus RTU/TCP, OPC UA Information Models & TSN`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 16 (Serial & Busses), Chapter 33 (Modbus & OPC UA).
- **Ruang Lingkup & Batasan**: Polling Modbus deterministik, pemetaan register Holding/Input ke tipe data IEEE 754 float32, perancangan NodeSet XML ruang alamat OPC UA (Object, Variable, Method, Event), dan dasar komunikasi *Time-Sensitive Networking* (IEEE 802.1Qbv). Batasan: konfigurasi switch TSN perangkat keras proprietary disimulasikan melalui kernel Linux traffic control (`tc`).
- **Capaian Pembelajaran (LO)**:
  1. Mengonstruksi pohon hierarki objek dan tipe data industri terstruktur pada server OPC UA.
  2. Mengoptimalkan siklus polling bus Modbus RTU multi-drop RS-485 untuk mencegah kehabisan waktu (*timeout*).
- **Topik Teori Utama**: Standar transmisi EIA/TIA-485 balanced line, struktur paket Modbus Application Protocol, model informasi OPC UA IEC 62541, dan prinsip pertukaran data publish-subscribe OPC UA PubSub.
- **Landasan Matematis (KaTeX)**:
  - Waktu siklus total polling $M$ perangkat slave pada bus RS-485:
    $$
    T_{\text{cycle}} = \sum_{k=1}^{M} \left( T_{\text{req}, k} + t_{\text{resp\_turnaround}, k} + T_{\text{resp}, k} + t_{3{,}5} \right)
    $$
- **Worked Numerical Example**: Menghitung refresh rate maksimum dari 16 power meter pada bus RS-485 (baud rate 19200 bps) yang masing-masing meminta 20 holding register float32.
- **Eksperimen Komputasi**: Pembangunan server OPC UA Python yang memetakan telemetri sensor getaran Modbus RTU ke dalam struktur standar mesin perkakas.
- **Deliverables & Asesmen**: Berkas skema XML OPC UA NodeSet dan log validasi kepatuhan pertukaran data deterministik.
- **Rujukan Primer**: IEC 62541-5 (OPC UA Information Model); Modbus Application Protocol Specification v1.1b3.

### Modul B04: Time & Frequency Domain Feature Engineering for Rotating Machinery
- **Kode & Judul**: `B04 — Time & Frequency Domain Feature Engineering for Rotating Machinery`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 05, Chapter 35 (Edge AI).
- **Ruang Lingkup & Batasan**: Ekstraksi fitur statistik tingkat tinggi (Kurtosis, Skewness, Crest Factor, Shape Factor), transformasi domain frekuensi via FFT (*Fast Fourier Transform*), analisis spektrum selubung (*Envelope Demodulation*) via Transformasi Hilbert untuk mendeteksi cacat bearing, dan pelacakan frekuensi karakteristik kerusakan bantalan (BPFO, BPFI, BSF, FTF).
- **Capaian Pembelajaran (LO)**:
  1. Menghitung frekuensi karakteristik cacat mekanis bantalan gelinding berdasarkan geometri fisik bearing.
  2. Mengimplementasikan algoritma modulasi selubung (*envelope analysis*) untuk mengekstraksi benturan impak mikro berulang yang tertutup derau mesin normal.
- **Topik Teori Utama**: Karakteristik statistik momen ke-3 dan ke-4, Transformasi Hilbert dan pembentukan sinyal analitik, resonansi struktural frekuensi tinggi, dan dekomposisi frekuensi harmonik poros.
- **Landasan Matematis (KaTeX)**:
  - Perhitungan Kurtosis (indikator sensitif benturan impak lokal):
    $$
    \text{Kurtosis} = \frac{\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^4}{\left( \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2 \right)^2}
    $$
  - Frekuensi cacat cincin luar bantalan (*Ball Pass Frequency Outer Race* / BPFO):
    $$
    \text{BPFO} = \frac{n_{\text{balls}}}{2} \cdot f_r \cdot \left( 1 - \frac{d_{\text{ball}}}{D_{\text{pitch}}} \cos \beta \right)
    $$
- **Worked Numerical Example**: Diberikan bantalan dengan 9 bola gelinding berdiameter $d_{\text{ball}} = 12\text{ mm}$, diameter pitch $D_{\text{pitch}} = 65\text{ mm}$, sudut kontak $\beta = 0^\circ$, berputar pada kecepatan poros 1800 RPM ($f_r = 30\text{ Hz}$). Hitung frekuensi BPFO dan tentukan komponen spektral yang harus dipantau!
- **Eksperimen Komputasi**: Modul analisis Python yang memproses rekaman akselerasi getaran riil/sintetis, menghitung kurtosis, dan memetakan puncak spektrum selubung Hilbert.
- **Deliverables & Asesmen**: Kode modul ekstraksi fitur dan laporan diagnosis spektral anomali bantalan.
- **Rujukan Primer**: Randall, R. B., *Vibration-based Condition Monitoring: Industrial, Automotive and Aerospace Applications*, Wiley, 2021.

### Modul B05: Industrial Reliability, Functional Safety (SIL/IEC 61508) & Safe State Control
- **Kode & Judul**: `B05 — Industrial Reliability, Functional Safety (SIL/IEC 61508) & Safe State Control`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 20 (Reliability), Chapter 38 (Fault Injection).
- **Ruang Lingkup & Batasan**: Konsep keselamatan fungsional (*Functional Safety*), penentuan Safety Integrity Level (SIL 1 hingga SIL 4), arsitektur redundansi hardware (1oo1, 1oo2, 2oo3 voting), perhitungan probabilitas kegagalan rata-rata saat permintaan (*Probability of Failure on Demand* / PFD), dan rangkaian pemutus darurat (*Safety Instrumented System* / SIS).
- **Capaian Pembelajaran (LO)**:
  1. Menghitung fraksi kegagalan aman (*Safe Failure Fraction* / SFF) dan estimasi nilai SIL suatu arsitektur instrumentasi.
  2. Merancang algoritma voting 2-out-of-3 (2oo3) untuk penutupan katup kritis tanpa memicu penghentian palsu pabrik (*spurious trip*).
- **Topik Teori Utama**: Standar IEC 61508 / IEC 61511, laju kegagalan $\lambda$ (komponen aman $\lambda_s$ vs berbahaya $\lambda_d$), cakupan diagnostik (*Diagnostic Coverage* / DC), dan kurva keandalan bathtub.
- **Landasan Matematis (KaTeX)**:
  - Perhitungan Fraksi Kegagalan Aman (*Safe Failure Fraction*):
    $$
    \text{SFF} = \frac{\sum \lambda_s + \sum \lambda_{dd}}{\sum \lambda_s + \sum \lambda_d}
    $$
  - Probabilitas Kegagalan Rata-Rata pada Permintaan untuk arsitektur 1oo2 dengan interval uji berkala $T_I$:
    $$
    \text{PFD}_{\text{avg, 1oo2}} \approx \frac{\lambda_{du}^2 \cdot T_I^2}{3} + \beta \cdot \frac{\lambda_{du} \cdot T_I}{2}
    $$
- **Worked Numerical Example**: Menghitung $\text{PFD}_{\text{avg}}$ sensor temperatur industri redundant 1oo2 dengan $\lambda_{du} = 10^{-6}\text{ jam}^{-1}$, faktor kegagalan penyebab bersama $\beta = 0{,}02$, dan interval proof-test $T_I = 8760\text{ jam}$ (1 tahun), serta menentukan apakah sistem memenuhi target SIL 2.
- **Eksperimen Komputasi**: Simulasi perangkat lunak logika voting triple-modular redundancy (TMR) dan injeksi kegagalan transien sensor.
- **Deliverables & Asesmen**: Laporan evaluasi kuantitatif keselamatan fungsional sistem instrumentasi pabrik.
- **Rujukan Primer**: IEC 61508 Parts 1–7 (Functional Safety); Smith, D. J., *Reliability, Maintainability and Risk*.

### Modul B06: Capstone — Edge Predictive Maintenance System with High-Speed Sampling
- **Kode & Judul**: `B06 — Capstone: Edge Predictive Maintenance System with High-Speed Sampling`
- **Kedalaman Akademik**: **L4: Research Preparation**
- **Prasyarat Kurikulum Inti**: Seluruh modul B01–B05, Chapter 30, Chapter 40.
- **Spesifikasi & Rincian**: Dijabarkan secara mendalam pada Seksi 7 (Capstone Design).

---

## 4. Track C — Smart Agriculture & Environmental Monitoring

**Target Kompetensi Track**: Membangun dan mengevaluasi sistem pemantauan lingkungan terdistribusi (*Distributed Environmental Monitoring*) berskala lansekap yang tangguh terhadap cuaca ekstrem, hemat energi berbasis pemanen energi mikro (*Energy Harvesting*), mengoptimalkan tautan nirkabel jarak jauh LoRaWAN/satelit, serta menyajikan analitik evapotranspirasi presisi untuk efisiensi sumber daya air.

### Modul C01: Agro-Ecological System Modeling & In-Situ Sensing Constraints
- **Kode & Judul**: `C01 — Agro-Ecological System Modeling & In-Situ Sensing Constraints`
- **Kedalaman Akademik**: **L2: Undergraduate Complete**
- **Prasyarat Kurikulum Inti**: Chapter 01, Chapter 03 (Electronics Foundations), Chapter 07 (Analog Sensors).
- **Ruang Lingkup & Batasan**: Karakteristik fisik lingkungan pertanian (suhu tanah bertingkat, kelembaban volumetrik $\text{VWC}$, konduktivitas listrik $\text{EC}$, radiasi matahari PAR). Batasan degradasi sensor in-situ: korosi galvanik pada probe tanah, bio-fouling, dan fluktuasi salinitas tanah. Tidak mencakup pemodelan biokimia genetika tanaman.
- **Capaian Pembelajaran (LO)**:
  1. Menganalisis kurva karakteristik retensi air tanah (*Soil Water Retention Curve*) untuk menentukan titik layu permanen dan kapasitas lapang.
  2. Menerapkan teknik eksitasi AC berfrekuensi tinggi untuk meminimalkan polarisasi dan korosi pada elektroda sensor tanah.
- **Topik Teori Utama**: Fisika konduktivitas volumetrik tanah, sensor dielektrik TDR (*Time Domain Reflectometry*) dan FDR (*Frequency Domain Reflectometry*), hukum van 't Hoff pengaruh suhu terhadap konduktivitas, dan rancang bangun enclosure tahan air rating IP67/IP68.
- **Landasan Matematis (KaTeX)**:
  - Persamaan Topp (hubungan permitivitas relatif dielektrik tanah $\epsilon_r$ terhadap kadar air volumetrik $\theta$):
    $$
    \theta = -5{,}3 \times 10^{-2} + 2{,}92 \times 10^{-2} \epsilon_r - 5{,}5 \times 10^{-4} \epsilon_r^2 + 4{,}3 \times 10^{-6} \epsilon_r^3
    $$
- **Worked Numerical Example**: Menghitung kadar air tanah volumetrik $\theta$ jika pengukuran permitivitas dielektrik tanah terukur adalah $\epsilon_r = 18{,}4$, dan menentukan apakah kelembaban berada di atas kapasitas lapang ($\theta_{\text{field}} = 0{,}28$).
- **Eksperimen Komputasi**: Model kalibrasi polinomial multi-titik sensor kelembaban tanah terhadap temperatur tanah aktual.
- **Deliverables & Asesmen**: Kurva kalibrasi empiris sensor kelembaban tanah terkompensasi suhu.
- **Rujukan Primer**: Topp, G. C., et al., *Electromagnetic Determination of Soil Water Content*, Water Resources Research, 1980; ISO 11271 (Soil Quality — Determination of Redox Potential).

### Modul C02: Precision In-Situ Calibration, Temperature Drift & Sensor Aging Physics
- **Kode & Judul**: `C02 — Precision In-Situ Calibration, Temperature Drift & Sensor Aging Physics`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 07 (ADC & Filtering), Chapter 10 (Embedded Capstone).
- **Ruang Lingkup & Batasan**: Fenomena pergeseran nol (*zero drift*) dan pergeseran rentang (*span drift*) pada sensor elektrokimia gas ($\text{CO}_2, \text{NH}_3$) dan sensor kelembaban relatif berbasis kapasitif. Kalibrasi dua titik in-situ (*Two-Point Field Calibration*) dan kompensasi penuaan sensor (*Aging Compensation*).
- **Capaian Pembelajaran (LO)**:
  1. Memformulasikan matriks kompensasi suhu non-linear multi-variabel untuk sensor gas lingkungan.
  2. Mengimplementasikan algoritma kalibrasi baseline otomatis (*Automatic Baseline Correction* / ABC) pada simpul sensor beroperasi jangka panjang.
- **Topik Teori Utama**: Karakteristik koefisien suhu resistansi/kapasitansi, histeresis adsorpsi kelembaban, drift kimia jangka panjang, dan standar metrologi ISO/IEC Guide 98-3 (GUM).
- **Landasan Matematis (KaTeX)**:
  - Model kompensasi drift linier terhadap waktu dan suhu:
    $$
    V_{\text{corrected}} = \frac{V_{\text{raw}} - \left( V_0 + \alpha_T (T - T_{\text{ref}}) + \gamma_t \cdot t \right)}{1 + \beta_T (T - T_{\text{ref}})}
    $$
- **Worked Numerical Example**: Koreksi nilai pembacaan sensor kualitas udara yang mengalami kenaikan suhu dari $T_{\text{ref}} = 25^\circ\text{C}$ ke $38^\circ\text{C}$ dengan koefisien drift suhu $\alpha_T = 2{,}4\text{ mV/}^\circ\text{C}$ dan laju penuaan $\gamma_t = 0{,}05\text{ mV/hari}$ setelah 180 hari di lapangan.
- **Eksperimen Komputasi**: Script pemulihan nilai kalibrasi dari dataset deret waktu sensor lingkungan yang mengalami drifting suhu ekstrem.
- **Deliverables & Asesmen**: Pustaka modul Python algoritma koreksi drift otomatis dan estimasi ketidakpastian baku pengukuran.
- **Rujukan Primer**: JCGM 100:2008 (Guide to the Expression of Uncertainty in Measurement); WMO-No. 8 (Guide to Meteorological Instruments and Methods of Observation).

### Modul C03: LoRaWAN Topography Planning, Fresnel Zone & Canopy Path Loss Modeling
- **Kode & Judul**: `C03 — LoRaWAN Topography Planning, Fresnel Zone & Canopy Path Loss Modeling`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 12 (Propagation), Chapter 18 (LoRa & LPWAN).
- **Ruang Lingkup & Batasan**: Perencanaan propagasi radio LoRaWAN pada frekuensi sub-GHz ($915\text{ MHz} / 920\text{ MHz}$ AS923) melintasi lanskap perkebunan/hutan. Pemodelan redaman dedaunan pohon (*Canopy Attenuation*), klirens Zona Fresnel pertama, difraksi tepi pisau (*Knife-Edge Diffraction*), dan optimasi Spreading Factor (SF7 hingga SF12).
- **Capaian Pembelajaran (LO)**:
  1. Menghitung radius klirens Zona Fresnel ke-1 pada bentang jarak transmisi sensor pertanian ke gateway.
  2. Menganalisis redaman tambahan akibat kanopi tanaman kelapa sawit/karet menggunakan model Weissberger.
- **Topik Teori Utama**: Rekomendasi ITU-R P.833 (Attenuation in vegetation), geometri propagasi gelombang elektromagnetik terrestrial, model elevasi digital (DEM/SRTM), dan batasan regulasi EIRP serta duty cycle spektrum tak berlisensi.
- **Landasan Matematis (KaTeX)**:
  - Radius Zona Fresnel pertama pada titik $P$ berjarak $d_1$ dan $d_2$:
    $$
    r_1 = \sqrt{\frac{\lambda \cdot d_1 \cdot d_2}{d_1 + d_2}}
    $$
  - Model Redaman Vegetasi Weissberger (untuk ketebalan dedaunan $d_v$ meter pada frekuensi $f$ GHz):
    $$
    L_{\text{veg, dB}} = 1{,}33 \cdot f^{0{,}284} \cdot d_v^{0{,}588} \quad (\text{untuk } 14 < d_v \le 400\text{ m})
    $$
- **Worked Numerical Example**: Menghitung tinggi tiang antena gateway yang dibutuhkan untuk menjamin klirens $60\%$ Zona Fresnel pada bentang jarak $5\text{ km}$ ($f = 920\text{ MHz}$) yang terhalang bukit di tengah lintasan ($d_1 = d_2 = 2{,}5\text{ km}$), ditambah redaman tajuk pohon setebal $30\text{ meter}$.
- **Eksperimen Komputasi**: Tool simulasi profil elevasi medan dan estimasi Link Budget radio LoRaWAN komprehensif.
- **Deliverables & Asesmen**: Laporan perencanaan penempatan gateway dan peta jangkauan coverage margin nirkabel perkebunan.
- **Rujukan Primer**: ITU-R Recommendation P.833-10; LoRa Alliance, *LoRaWAN Regional Parameters v1.0.3*.

### Modul C04: Energy Harvesting, Solar Irradiance Profiling & Supercapacitor Dimensioning
- **Kode & Judul**: `C04 — Energy Harvesting, Solar Irradiance Profiling & Supercapacitor Dimensioning`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 31 (Low-Power & Sleep Modes).
- **Ruang Lingkup & Batasan**: Perancangan catu daya mandiri (*Energy-Autonomous Node*) memadukan panel fotovoltaik mikro (PV 5V, 100–500 mW), sirkuit MPPT (*Maximum Power Point Tracking*) berbasis induktor mikro, superkapasitor vs baterai $\text{LiFePO}_4$, dan algoritma pengelolaan konsumsi energi adaptif terhadap musim cuaca buruk berhari-hari (*Days of Autonomy*).
- **Capaian Pembelajaran (LO)**:
  1. Menghitung dimensi kapasitas superkapasitor dan baterai penyimpan untuk menjamin operasional kontinu selama $k$ hari berawan/hujan.
  2. Menerapkan kontrol duty cycle sampling dinamis berbasis pemantauan status tegangan kapasitor penampung daya.
- **Topik Teori Utama**: Karakteristik kurva I-V panel PV, efisiensi sirkuit pemanen energi (misal arsitektur Texas Instruments BQ25570), model kebocoran arus superkapasitor (*Self-Discharge*), dan strategi *Energy-Neutral Operation* (ENO).
- **Landasan Matematis (KaTeX)**:
  - Dimensi kapasitas superkapasitor $C_{\text{super}}$ untuk menyuplai energi $E_{\text{req}}$ antara batas tegangan kerja $V_{\text{max}}$ dan $V_{\text{min}}$:
    $$
    E_{\text{stored}} = \frac{1}{2} C_{\text{super}} \left( V_{\text{max}}^2 - V_{\text{min}}^2 \right) \implies C_{\text{super}} = \frac{2 \cdot E_{\text{req}}}{V_{\text{max}}^2 - V_{\text{min}}^2}
    $$
- **Worked Numerical Example**: Node LoRaWAN membutuhkan energi rata-rata harian $E_{\text{req}} = 145\text{ Joule}$ (arus tidur $5\,\mu\text{A}$, transmisi paket 15 menit sekali). Jika superkapasitor diisi hingga $V_{\text{max}} = 5{,}0\text{ V}$ dan regulator LDO dapat bekerja hingga $V_{\text{min}} = 3{,}0\text{ V}$, hitung kapasitansi farad yang dibutuhkan untuk otonomi 48 jam tanpa sinar matahari!
- **Eksperimen Komputasi**: Simulasi kesetimbangan energi tahunan simpul sensor berbasis data historis radiasi matahari global (Solar Irradiance CSV).
- **Deliverables & Asesmen**: Skrip kalkulator dimensi catu daya surya dan grafik fluktuasi muatan energi sepanjang tahun.
- **Rujukan Primer**: Kansal, A., et al., *Power Management in Energy Harvesting Sensor Networks*, ACM Transactions on Embedded Computing Systems, 2007; IEC 61427 (Secondary cells and batteries for renewable energy storage).

### Modul C05: Evapotranspiration Analytics, FAO-56 Penman-Monteith & Precision Irrigation
- **Kode & Judul**: `C05 — Evapotranspiration Analytics, FAO-56 Penman-Monteith & Precision Irrigation`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 21 (Data Models), Chapter 23 (Edge Processing), Chapter 26 (Alerting).
- **Ruang Lingkup & Batasan**: Pemodelan kebutuhan air tanaman presisi (*Crop Water Requirement*) melalui perhitungan laju evapotranspirasi acuan ($\text{ET}_0$) standar FAO-56 Penman-Monteith, estimasi koefisien tanaman ($K_c$), neraca air tanah (*Soil Water Balance*), dan otomasi penjadwalan irigasi defisit terkendali. Batasan: aktuasi pompa hidrolik skala besar disimulasikan melalui aktuator katup solenoid biner.
- **Capaian Pembelajaran (LO)**:
  1. Menghitung nilai $\text{ET}_0$ harian dari data telemetri iklim mikro (suhu, radiasi netto, kecepatan angin, dan tekanan uap air).
  2. Merancang algoritma otomasi irigasi tertutup (*Closed-Loop Irrigation*) yang mengembalikan kandungan air tanah tepat pada tingkat kapasitas lapang tanpa pemborosan *deep percolation*.
- **Topik Teori Utama**: Persamaan FAO-56 Penman-Monteith, radiasi gelombang pendek & panjang netto, gradien tekanan uap jenuh udara, konsep fraksi penipisan air tanah mudah diserap (*Management Allowed Depletion* / MAD), dan pengendalian irigasi cerdas.
- **Landasan Matematis (KaTeX)**:
  - Persamaan Evapotranspirasi Acuan FAO-56 Penman-Monteith:
    $$
    \text{ET}_0 = \frac{0{,}408 \Delta (R_n - G) + \gamma \frac{900}{T + 273} u_2 (e_s - e_a)}{\Delta + \gamma (1 + 0{,}34 u_2)}
    $$
    di mana $R_n$ adalah radiasi netto, $G$ fluks panas tanah, $T$ suhu rata-rata, $u_2$ kecepatan angin pada ketinggian 2 m, $(e_s - e_a)$ defisit tekanan uap, $\Delta$ kemiringan kurva tekanan uap, dan $\gamma$ konstanta psikrometrik.
- **Worked Numerical Example**: Perhitungan langkah-demi-langkah $\text{ET}_0$ pada hari cerah tropis ($T = 28^\circ\text{C}$, $R_n = 16{,}5\text{ MJ/m}^2/\text{hari}$, $u_2 = 1{,}8\text{ m/s}$, $\text{RH} = 70\%$) dan penentuan durasi bukaan katup tetes ($Q_{\text{emitter}} = 4\text{ L/jam}$) untuk blok lahan $100\text{ m}^2$.
- **Eksperimen Komputasi**: Modul Python perhitungan neraca air tanah harian terintegrasi dengan trigger aktuasi irigasi prediktif.
- **Deliverables & Asesmen**: Laporan efisiensi konservasi air simulasi irigasi cerdas vs irigasi timer konvensional.
- **Rujukan Primer**: Allen, R. G., et al., *Crop Evapotranspiration — Guidelines for Computing Crop Water Requirements — FAO Irrigation and Drainage Paper 56*, United Nations FAO, Rome, 1998.

### Modul C06: Capstone — Autonomous LoRaWAN Agricultural Microclimate Network
- **Kode & Judul**: `C06 — Capstone: Autonomous LoRaWAN Agricultural Microclimate Network`
- **Kedalaman Akademik**: **L4: Research Preparation**
- **Prasyarat Kurikulum Inti**: Seluruh modul C01–C05, Chapter 30, Chapter 40.
- **Spesifikasi & Rincian**: Dijabarkan secara mendalam pada Seksi 7 (Capstone Design).

---

## 5. Track D — AIoT & Edge Intelligence

**Target Kompetensi Track**: Mengintegrasikan unit komputasi tertanam berdaya rendah dengan teknik machine learning modern; mencakup pipeline akuisisi sinyal berkecepatan tinggi, ekstraksi fitur domain waktu/frekuensi, arsitektur model TinyML kompak, teknik kompresi model kuantisasi fixed-point INT8/INT4 dan pruning terstruktur, fusi sensor multimodal Kalman/Bayesian, serta pemantauan pergeseran data konsep (*concept drift*) di tepi jaringan.

### Modul D01: Embedded AI Architecture, Hardware Accelerators & Neural Processing Units (NPUs)
- **Kode & Judul**: `D01 — Embedded AI Architecture, Hardware Accelerators & Neural Processing Units (NPUs)`
- **Kedalaman Akademik**: **L2: Undergraduate Complete**
- **Prasyarat Kurikulum Inti**: Chapter 04 (ESP32/MCU), Chapter 05 (C/C++ & Memory).
- **Ruang Lingkup & Batasan**: Arsitektur perangkat keras prosesor mikrokontroler modern dengan akselerator kecerdasan buatan terintegrasi (ARM Cortex-M55/M85 dengan instruksi Helium/MVE, ESP32-S3 dengan instruksi vektor Xtensa, dan mikro-NPU seperti Ethos-U55). Analisis arsitektur memori tight-coupled (TCM), batasan bandwidth SRAM internal, dan throughput per watt.
- **Capaian Pembelajaran (LO)**:
  1. Membedakan pemrosesan tensor pada arsitektur CPU murni, SIMD integer, dan Neural Processing Unit (NPU) terdedikasi.
  2. Menganalisis batas batas memori (*Roofline Model*) komputasi neural network pada mikrokontroler.
- **Topik Teori Utama**: Ekstensi instruksi SIMD vektor, arsitektur systolic array pada mikro-NPU, hierarki memori embedded (Flash vs PSRAM vs SRAM vs TCM), dan model performa Roofline (Memory Bandwidth vs Compute Peak Bound).
- **Landasan Matematis (KaTeX)**:
  - Model Roofline batas throughput komputasi:
    $$
    P = \min \left( P_{\text{peak}}, \quad I_{\text{arith}} \cdot B_{\text{mem}} \right)
    $$
    di mana $P$ adalah kinerja (MAC/detik), $I_{\text{arith}}$ intensitas aritmatika (FLOPs/byte transfer memori), dan $B_{\text{mem}}$ bandwidth antarmuka memori (byte/detik).
- **Worked Numerical Example**: Menentukan apakah eksekusi layer konvolusi 1D ($I_{\text{arith}} = 1{,}8\text{ MAC/byte}$) pada prosesor berkecepatan $400\text{ MHz}$ ($P_{\text{peak}} = 800\text{ MMAC/s}$) dengan bandwidth memori Flash SPI $B_{\text{mem}} = 80\text{ MB/s}$ dibatasi oleh memori (*memory-bound*) atau komputasi (*compute-bound*).
- **Eksperimen Komputasi**: Benchmark waktu eksekusi perkalian dot product float32 vs operasi vektor integer terakselerasi SIMD pada emulasi mikroprosesor.
- **Deliverables & Asesmen**: Laporan evaluasi pemakaian memori dan grafik Roofline untuk beberapa layer neural network.
- **Rujukan Primer**: Asanović, K., et al., *The Landscape of Parallel Computing Research: A View from Berkeley*; Arm Ltd, *Arm Helium Technology Reference Manual*.

### Modul D02: Edge Feature Engineering, Signal Preprocessing & Dimensionality Reduction
- **Kode & Judul**: `D02 — Edge Feature Engineering, Signal Preprocessing & Dimensionality Reduction`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 05, Chapter 23 (Edge Processing), Chapter 35 (Edge AI).
- **Ruang Lingkup & Batasan**: Transformasi sinyal waktu nyata langsung di memori SRAM penyangga (*streaming pipeline*): Filter IIR/FIR filter integer, perancangan bank filter Mel-Scale (MFCC) untuk pengenalan audio/suara mikro, dekomposisi gelombang wavelet diskrit (DWT), dan reduksi dimensi Principal Component Analysis (PCA) fixed-point.
- **Capaian Pembelajaran (LO)**:
  1. Mengimplementasikan ekstraksi koefisien Mel-Frequency Cepstral Coefficients (MFCC) menggunakan representasi aritmatika fixed-point integer 16-bit.
  2. Merancang filter lolos-pita digital IIR Butterworth hemat siklus instruksi untuk pra-kondisi data getaran/akustik.
- **Topik Teori Utama**: Teorema sampling diskrit, transformasi waktu-frekuensi, transformasi kosinus diskrit (DCT), filter bank segitiga skala Mel, dan trade-off presisi numerik fixed-point Q-format ($Q15 / Q31$).
- **Landasan Matematis (KaTeX)**:
  - Konversi frekuensi linier $f$ (Hz) ke skala subjektif Mel $m$:
    $$
    m = 2595 \log_{10} \left( 1 + \frac{f}{700} \right)
    $$
  - Filter IIR orde-dua (Biquad difference equation):
    $$
    y[n] = b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] - a_1 y[n-1] - a_2 y[n-2]
    $$
- **Worked Numerical Example**: Perhitungan koefisien biquad dan kuantisasi fixed-point $Q15$ dari filter lolos-rendah IIR cut-off $50\text{ Hz}$ pada frekuensi sampling $1000\text{ Hz}$, serta evaluasi noise lantai kuantisasi.
- **Eksperimen Komputasi**: Modul C/Python streaming MFCC extractor dari rekaman audio anomali suara bantalan mesin.
- **Deliverables & Asesmen**: Pipeline pra-pemrosesan sinyal stream dengan verifikasi ketiadaan memory leak.
- **Rujukan Primer**: Oppenheim, A. V., & Schafer, R. W., *Discrete-Time Signal Processing*, Pearson; Davis, S., & Mermelstein, P., *Comparison of Parametric Representations for Monosyllabic Word Recognition*, IEEE ASSP, 1980.

### Modul D03: Deep TinyML: Quantization-Aware Training (QAT), Structured Pruning & Knowledge Distillation
- **Kode & Judul**: `D03 — Deep TinyML: Quantization-Aware Training (QAT), Structured Pruning & Knowledge Distillation`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 35 (Edge AI TinyML).
- **Ruang Lingkup & Batasan**: Metode kompresi model canggih melampaui Post-Training Quantization (PTQ) standar: *Quantization-Aware Training* (QAT) dengan simulasi galat pembulatan saat backpropagation, pemangkasan bobot berstruktur (*Structured Channel Pruning*), dan distilasi pengetahuan (*Knowledge Distillation*) dari model guru besar (*Teacher*) ke model siswa mikro (*Student*).
- **Capaian Pembelajaran (LO)**:
  1. Melatih jaringan saraf konvolusi mikro menggunakan QAT untuk mempertahankan akurasi klasifikasi pada kuantisasi INT8 penuh.
  2. Menerapkan distilasi pengetahuan loss Kullback-Leibler divergence untuk mentransfer representasi fitur kompleks ke arsitektur jaringan kompak.
- **Topik Teori Utama**: Prinsip Straight-Through Estimator (STE) pada QAT, kompresi matriks jarang (*sparse matrix*), fungsi kerugian suhu distilasi Hinton, dan konversi model ke format biner TFLite Micro FlatBuffers.
- **Landasan Matematis (KaTeX)**:
  - Fungsi objektif komposit distilasi pengetahuan:
    $$
    \mathcal{L}_{\text{total}} = (1 - \alpha) \cdot \mathcal{L}_{\text{CE}}(y, \sigma(z_s)) + \alpha \cdot T^2 \cdot \mathcal{L}_{\text{KL}}\left( \sigma\left(\frac{z_s}{T}\right), \sigma\left(\frac{z_t}{T}\right) \right)
    $$
    di mana $z_s, z_t$ adalah logits student dan teacher, $T$ temperatur pelunakan, dan $\mathcal{L}_{\text{KL}}$ divergensi Kullback-Leibler.
- **Worked Numerical Example**: Perhitungan gradien pembaruan bobot STE pada neuron terkuantisasi saat nilai float berada di dalam rentang saturasi clipping $[-128, 127]$ versus saat berada di luar batas saturasi.
- **Eksperimen Komputasi**: Pipeline pelatihan model PyTorch/TensorFlow dengan QAT dan pemangkasan $50\%$ parameter filter konvolusi tanpa degradasi akurasi signifikan.
- **Deliverables & Asesmen**: Notebook pelatihan model QAT dan berkas model tflite biner siap-flash berserta profil akurasi vs ukuran memori.
- **Rujukan Primer**: Jacob, B., et al., *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*, IEEE CVPR, 2018; Hinton, G., et al., *Distilling the Knowledge in a Neural Network*, NIPS Deep Learning Workshop, 2014.

### Modul D04: Multimodal Sensor Fusion, Bayesian Estimation & Extended Kalman Filters
- **Kode & Judul**: `D04 — Multimodal Sensor Fusion, Bayesian Estimation & Extended Kalman Filters`
- **Kedalaman Akademik**: **L4: Research Preparation**
- **Prasyarat Kurikulum Inti**: Chapter 07, Chapter 23, Chapter 36 (Digital Twin).
- **Ruang Lingkup & Batasan**: Fusi data multi-sensor heterogen (misalnya akselerometer + giroskop + magnetometer untuk estimasi orientasi AHRS, atau sensor suhu kontak + inframerah non-kontak + fluks daya). Formulasi filter komplementer, filter Kalman linier (KF), dan *Extended Kalman Filter* (EKF) untuk sistem dinamik non-linear terdiskritisasi pada prosesor mikro.
- **Capaian Pembelajaran (LO)**:
  1. Menurunkan matriks kovarians galat dan matriks penguatan Kalman (*Kalman Gain*) untuk fusi dua sensor dengan karakteristik derau berbeda.
  2. Mengimplementasikan algoritma EKF pada mikrokontroler dengan komputasi inversi matriks berorde rendah yang stabil secara numerik.
- **Topik Teori Utama**: Estimasi status state-space linier dan non-linear, derau proses kuadratik $Q$ dan derau pengukuran $R$, linearisasi deret Taylor derifatif matriks Jacobian, dan parameterisasi kuaternion rotasi 3D.
- **Landasan Matematis (KaTeX)**:
  - Siklus Pembaruan Koreksi Filter Kalman:
    $$
    K_k = P_k^- H_k^T \left( H_k P_k^- H_k^T + R_k \right)^{-1}
    $$
    $$
    \hat{x}_k = \hat{x}_k^- + K_k \left( z_k - h(\hat{x}_k^-) \right)
    $$
    $$
    P_k = (I - K_k H_k) P_k^-
    $$
- **Worked Numerical Example**: Fusi estimasi temperatur inti reaktor baterai menggunakan model termal internal ($R_{\text{model}} = 0{,}8$) dan pembacaan sensor termokopel eksternal ($R_{\text{meas}} = 0{,}2$). Hitung penguatan Kalman $K$ dan estimasi status baru saat deviasi inovasi pengukuran sebesar $+3{,}5^\circ\text{C}$.
- **Eksperimen Komputasi**: Script simulasi Python fusi orientasi pitch-roll EKF 6-DOF IMU dengan injeksi derau Gauss dan bias getaran.
- **Deliverables & Asesmen**: Implementasi modul fusi sensor EKF dan analisis komparasi konvergensi terhadap filter komplementer sederhana.
- **Rujukan Primer**: Kalman, R. E., *A New Approach to Linear Filtering and Prediction Problems*, Journal of Basic Engineering, 1960; Farrell, J., *Aided Navigation: GPS with High Rate Sensors*, McGraw-Hill.

### Modul D05: Edge AI Model Lifecycle: Deployment, Benchmarking, Quantization Drift & On-Device Anomaly Tracking
- **Kode & Judul**: `D05 — Edge AI Model Lifecycle: Deployment, Benchmarking, Quantization Drift & On-Device Anomaly Tracking`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 27 (Fleet Management), Chapter 29 (OTA & Observability), Chapter 35.
- **Ruang Lingkup & Batasan**: Pemantauan kesehatan siklus hidup (*Model Lifecycle MLOps at the Edge*) model kecerdasan buatan setelah diluncurkan ke ribuan perangkat: benchmarking latensi inferensi dan konsumsi arus riil, deteksi degradasi performa akibat perubahan distribusi data (*Data Drift & Concept Drift*), dan pelaporan ringkas metrik keyakinan model (*Confidence Score Telemetry*) tanpa melanggar privasi pengguna.
- **Capaian Pembelajaran (LO)**:
  1. Mengukur latensi inferensi per layer dan overhead alokasi memori arena menggunakan profiler TensorFlow Lite for Microcontrollers.
  2. Menerapkan uji statistik Kolmogorov-Smirnov atau Population Stability Index (PSI) berbasis jendela waktu geser untuk mendeteksi drift sensor di perangkat edge.
- **Topik Teori Utama**: Arsitektur eksekusi TFLite Micro interpreter, metrik kuantifikasi drift (PSI, Wasserstein Distance), pelaporan telemetri inferensi teragregasi, dan strategi pembaruan parsial bobot model melalui OTA delta patching.
- **Landasan Matematis (KaTeX)**:
  - Indeks Stabilitas Populasi (*Population Stability Index* / PSI):
    $$
    \text{PSI} = \sum_{b=1}^{B} \left( P_b - Q_b \right) \cdot \ln\left( \frac{P_b}{Q_b} \right)
    $$
    di mana $P_b$ adalah proporsi data aktual saat ini pada bin ke-$b$ dan $Q_b$ adalah proporsi data baseline saat model pertama dilatih. Batas drift: $\text{PSI} > 0{,}25$ menandakan pergeseran signifikan.
- **Worked Numerical Example**: Evaluasi PSI dari distribusi fitur RMS getaran motor pada 5 interval bin setelah 6 bulan operasi, membuktikan perlunya pembaruan bobot model.
- **Eksperimen Komputasi**: Harness benchmarking edge AI yang mengukur latensi CPU clock cycles per inferensi dan mengevaluasi metrik drift populasi sintetis.
- **Deliverables & Asesmen**: Laporan benchmarking performa inferensi dan modul deteksi drift berbasis ambang batas PSI.
- **Rujukan Primer**: Warden, P., & Situnayake, D., *TinyML*, O'Reilly; ISO/IEC 22989:2022 (Information technology — Artificial intelligence).

### Modul D06: Capstone — Real-Time Multimodal Edge Vision & Acoustic Anomaly Detection System
- **Kode & Judul**: `D06 — Capstone: Real-Time Multimodal Edge Vision & Acoustic Anomaly Detection System`
- **Kedalaman Akademik**: **L4: Research Preparation**
- **Prasyarat Kurikulum Inti**: Seluruh modul D01–D05, Chapter 30, Chapter 40.
- **Spesifikasi & Rincian**: Dijabarkan secara mendalam pada Seksi 7 (Capstone Design).

---

## 6. Track E — IoT for Telecommunications & Smart Cities

**Target Kompetensi Track**: Merancang, memodelkan, mengoptimalkan, dan mengevaluasi infrastruktur komunikasi nirkabel skala metropolitan (*City-Scale IoT Networks*); mencakup propagasi gelombang elektromagnetik terrestrial urban, perencanaan kapasitas tautan LPWAN (LoRaWAN/NB-IoT) dan seluler 4G/5G mMTC, analisis Quality of Service (QoS), ketahanan lalu lintas data masif (*massive telemetry ingestion*), serta tata kelola data perkotaan dan privasi publik.

### Modul E01: Smart City IoT Systems Engineering, Urban Topologies & Municipal Architecture
- **Kode & Judul**: `E01 — Smart City IoT Systems Engineering, Urban Topologies & Municipal Architecture`
- **Kedalaman Akademik**: **L2: Undergraduate Complete**
- **Prasyarat Kurikulum Inti**: Chapter 01, Chapter 02 (Architecture), Chapter 11 (Networking).
- **Ruang Lingkup & Batasan**: Arsitektur perkotaan terintegrasi (Smart Metering Listrik/Air, Lampu Penerangan Jalan Cerdas / PJU, Pemantauan Banjir Kanal Kota, dan Manajemen Parkir Terdistribusi). Topologi jaringan hirarki bertingkat: Simpul Lapangan $\to$ Gateway Seluler/Penerangan Jalan $\to$ Edge Aggregator Distrik $\to$ Municipal Cloud Command Center. Standar interoperabilitas data kota (ITU-T Y.4000 series, FIWARE Smart Data Models).
- **Capaian Pembelajaran (LO)**:
  1. Merancang topologi komunikasi data perkotaan yang memisahkan lalu lintas telemetri publik dan jaringan kendali layanan kritis.
  2. Menerapkan model ontologi data terstandar FIWARE NGSI-LD untuk integrasi antar-aplikasi dinas perkotaan.
- **Topik Teori Utama**: Rekomendasi ITU-T Y.4200 (IoT requirements for smart cities), standar antarmuka data ETSI ISG CIM (NGSI-LD API), hierarki ketersediaan layanan kota (*City Resilience Index*), dan topologi backhaul nirkabel/fiber-optic.
- **Landasan Matematis (KaTeX)**:
  - Model ketersediaan jaringan terdistribusi mesh perkotaan dengan $N$ gateway paralel:
    $$
    A_{\text{city}} = 1 - \prod_{i=1}^{N} (1 - A_{\text{gw}, i})
    $$
- **Worked Numerical Example**: Perhitungan probabilitas redundansi penerimaan sinyal meteran pintar di distrik kota dengan 4 gateway LoRaWAN independen (masing-masing memiliki reliabilitas link $90\%$).
- **Eksperimen Komputasi**: Pembangunan skema data JSON-LD / NGSI-LD entitas penerangan jalan pintar (*Smart Streetlight*) terintegrasi sensor lingkungan.
- **Deliverables & Asesmen**: Dokumen rancangan arsitektur data terbuka perkotaan dan skema entitas NGSI-LD tervalidasi.
- **Rujukan Primer**: ITU-T Y.4451 (Framework of constrained device management in smart cities); ETSI GS CIM 009 (NGSI-LD API).

### Modul E02: Urban RF Propagation, Empirical Path Loss Models & Multipath Fading Analysis
- **Kode & Judul**: `E02 — Urban RF Propagation, Empirical Path Loss Models & Multipath Fading Analysis`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 11, Chapter 12 (Propagation & Friis).
- **Ruang Lingkup & Batasan**: Propagasi gelombang radio nirkabel pada lingkungan urban padat (*Urban Clutter*): Model empiris Okumura-Hata, COST 231 Hata, dan 3GPP Urban Micro (UMi) path loss. Fenomena multipath fading (distribusi Rayleigh untuk kondisi Non-Line-of-Sight / NLoS dan Rician untuk Line-of-Sight / LoS), *shadowing* log-normal, serta perhitungan fading margin.
- **Capaian Pembelajaran (LO)**:
  1. Menghitung rugi-rugi lintasan propagasi gelombang elektromagnetik di lingkungan perkotaan menggunakan formula empiris COST 231 Hata.
  2. Memodelkan fluktuasi sinyal akibat multipath fading dan menentukan link margin yang diperlukan untuk keandalan penerimaan sinyal $99\%$.
- **Topik Teori Utama**: Karakteristik kanal nirkabel urban, tinggi efektif antena base station ($h_b$) dan terminal bergerak ($h_m$), distribusi Rayleigh dan Rician, deviasi standar log-normal shadowing ($\sigma_{\text{shadow}}$), dan persentase cakupan area.
- **Landasan Matematis (KaTeX)**:
  - Model Path Loss COST 231 Hata (Urban Area, $1500 < f \le 2000\text{ MHz}$):
    $$
    L_{\text{urban}} = 46{,}3 + 33{,}9 \log_{10}(f) - 13{,}82 \log_{10}(h_b) - a(h_m) + \left( 44{,}9 - 6{,}55 \log_{10}(h_b) \right) \log_{10}(d) + C_M
    $$
    di mana $C_M = 0\text{ dB}$ untuk kota menengah dan $3\text{ dB}$ untuk metropolitan metropolitan padat.
  - Fungsi kerapatan probabilitas Rayleigh fading envelope $r$:
    $$
    p(r) = \frac{r}{\sigma^2} e^{-\frac{r^2}{2\sigma^2}}, \qquad P(r \le R_{\text{th}}) = 1 - e^{-\frac{R_{\text{th}}^2}{2\sigma^2}}
    $$
- **Worked Numerical Example**: Menghitung path loss untuk gateway menara BTS telekomunikasi ($h_b = 30\text{ m}$) yang melayani simpul sensor pintar di permukaan jalan ($h_m = 1{,}5\text{ m}$) pada jarak $d = 2{,}5\text{ km}$ dengan frekuensi $1800\text{ MHz}$, serta menentukan fade margin untuk menjamin outage probability $< 1\%$.
- **Eksperimen Komputasi**: Script simulasi Monte Carlo untuk pemodelan envelope sinyal Rayleigh/Rician dan penentuan probabilitas putus koneksi (*outage*).
- **Deliverables & Asesmen**: Laporan studi propagasi radio seluler/LPWAN urban dan grafik distribusi sinyal terdisrupsi multipath.
- **Rujukan Primer**: Rappaport, T. S., *Wireless Communications: Principles and Practice*, 2nd Ed, Prentice Hall; 3GPP TR 38.901 (Study on channel model for frequencies from 0.5 to 100 GHz).

### Modul E03: Cellular IoT (NB-IoT & LTE-M), 3GPP Release Specifications & Link Adaptation
- **Kode & Judul**: `E03 — Cellular IoT (NB-IoT & LTE-M), 3GPP Release Specifications & Link Adaptation`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 11 (TCP/IP), Chapter 18 (LoRaWAN), Chapter 31 (Low-Power).
- **Ruang Lingkup & Batasan**: Standar telekomunikasi seluler 3GPP Release 13/14/15/16 khusus transmisi masif mesin (*massive Machine Type Communications* / mMTC): Narrowband IoT (NB-IoT Cat-NB1/NB2) dan LTE-M (Cat-M1/M2). Mode penghematan daya ekstensif: *Power Saving Mode* (PSM) dan *extended Discontinuous Reception* (eDRX). Peningkatan cakupan (*Coverage Enhancement* / CE Level 0, 1, 2) melalui teknik pengulangan transmisi paket (*packet repetition*).
- **Capaian Pembelajaran (LO)**:
  1. Menganalisis alokasi bandwidth sub-carrier NB-IoT (180 kHz / 1 PRB) pada mode operasi In-band, Guard-band, dan Standalone.
  2. Menghitung anggaran konsumsi energi siklus operasional perangkat seluler menggunakan konfigurasi timer PSM (T3324 dan T3412).
- **Topik Teori Utama**: Arsitektur E-UTRAN untuk seluler IoT, prosedur perlekatan jaringan (*Attach procedure*), mekanisme penangguhan status RRC (*RRC Connection Suspend/Resume*), dan perbandingan performa latensi/throughput LTE-M vs NB-IoT.
- **Landasan Matematis (KaTeX)**:
  - Peningkatan Maximum Coupling Loss (MCL) melalui pengulangan sub-frame transmisi paket sejumlah $N_{\text{rep}}$ kali:
    $$
    \Delta \text{SNR}_{\text{gain}} = 10 \log_{10}(N_{\text{rep}})
    $$
    Untuk $N_{\text{rep}} = 128$ kali pengulangan: $\Delta \text{SNR} \approx 21\text{ dB}$, menaikkan MCL dari $144\text{ dB}$ standar seluler ke $164\text{ dB}$ untuk tembus hingga ruang bawah tanah (*deep basement*).
- **Worked Numerical Example**: Perhitungan konsumsi energi baterai tahunan sensor meteran gas NB-IoT yang mengirimkan 1 paket (100 byte) setiap 24 jam dengan timer aktif $T3324 = 4\text{ detik}$, periode pelaporan $T3412 = 24\text{ jam}$, dan arus tidur PSM $I_{\text{psm}} = 3\,\mu\text{A}$.
- **Eksperimen Komputasi**: Script pemodelan siklus arus telekomunikasi seluler (Wakeup $\to$ Sync $\to$ Attach $\to$ Data $\to$ Tail Time $\to$ eDRX $\to$ PSM).
- **Deliverables & Asesmen**: Profil daya siklus transmisi modem seluler dan perbandingan trade-off Repetition vs Battery Lifetime.
- **Rujukan Primer**: 3GPP TS 36.300 (E-UTRA and E-UTRAN Overall description); Liberg, O., et al., *Cellular Internet of Things: From LMR, NB-IoT, and LTE-M to 5G*, Academic Press, 2019.

### Modul E04: Municipal Network Performance, Contention Modeling & SLA Assurance
- **Kode & Judul**: `E04 — Municipal Network Performance, Contention Modeling & SLA Assurance`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 14 (MQTT), Chapter 20 (Availability), Chapter 37 (Scalability).
- **Ruang Lingkup & Batasan**: Karakteristik performa jaringan IoT perkotaan yang melayani ratusan ribu simpul pemancar serentak. Model tumbukan kanal acak Pure ALOHA dan Slotted ALOHA pada LPWAN. Kapasitas kanal jenuh (*Saturated Throughput*), rasio keberhasilan paket (*Packet Delivery Ratio* / PDR), serta perancangan Service Level Agreement (SLA) untuk telemetri infrastruktur kota kritis vs non-kritis.
- **Capaian Pembelajaran (LO)**:
  1. Menghitung kapasitas muatan kanal maksimum dan probabilitas tabrakan paket pada jaringan acak skala besar menggunakan formulasi ALOHA.
  2. Merancang metrik SLA keterlambatan paket (*latency jitter*) dan availability untuk layanan publik dinas tata kota.
- **Topik Teori Utama**: Teori antrean Poisson, analisis beban kanal (*Traffic Load $G$*), interferensi sesama kanal (*Co-channel interference*), fenomena capture effect pada modulasi spread-spectrum, dan pembatasan regulasi duty cycle sub-GHz regional (misal $1\%$).
- **Landasan Matematis (KaTeX)**:
  - Throughput kanal ALOHA murni (*Pure ALOHA throughput*):
    $$
    S = G \cdot e^{-2G}
    $$
    Throughput teoritis maksimum: $S_{\text{max}} = \frac{1}{2e} \approx 0{,}184 \quad (18{,}4\%) \text{ pada } G = 0{,}5$.
  - Probabilitas sukses transmisi paket tanpa collision pada laju kedatangan agregat $\lambda$ dan durasi Time-on-Air $\tau_{\text{ToA}}$:
    $$
    P_{\text{succ}} = e^{-2 \lambda \tau_{\text{ToA}}}
    $$
- **Worked Numerical Example**: Sebuah gateway melayani $10.000$ unit sensor parkir pintar yang masing-masing mengirimkan paket dengan $\tau_{\text{ToA}} = 120\text{ ms}$ setiap interval rata-rata 300 detik. Hitung total traffic load $G$, throughput kanal $S$, dan probabilitas kehilangan paket akibat collision!
- **Eksperimen Komputasi**: Simulasi Monte Carlo diskrit peristiwa kedatangan paket ribuan node untuk memvalidasi batas saturasi ALOHA dan degradasi PDR.
- **Deliverables & Asesmen**: Laporan analitik kapasitas kanal kota dan model verifikasi pemenuhan SLA 99,5% paket sampai.
- **Rujukan Primer**: Abramson, N., *The ALOHA System — Another Alternative for Computer Communications*, AFIPS NCC, 1970; Adelantado, F., et al., *Understanding the Limits of LoRaWAN*, IEEE Communications Magazine, 2017.

### Modul E05: Geospatial Telemetry, Sensor Geofencing & Smart City Data Governance
- **Kode & Judul**: `E05 — Geospatial Telemetry, Sensor Geofencing & Smart City Data Governance`
- **Kedalaman Akademik**: **L3: Advanced Engineering**
- **Prasyarat Kurikulum Inti**: Chapter 21 (Data Models), Chapter 25 (Time-Series DB), Chapter 39 (Privacy & Governance).
- **Ruang Lingkup & Batasan**: Pengolahan data telemetri berkoordinat spasial (GNSS/GPS, estimasi posisi TDoA LoRaWAN, geocoding alamat fisik): Format GeoJSON terstandar, basis data spasial (PostGIS), algoritma *Ray-Casting* untuk penentuan titik di dalam poligon geofencing perkotaan, serta tata kelola privasi data publik (anonimisasi lokasi GPS armada kendaraan publik dan k-anonymity spasial).
- **Capaian Pembelajaran (LO)**:
  1. Mengimplementasikan algoritma geofencing spasial untuk mendeteksi deviasi rute kendaraan operasional kota secara real-time.
  2. Menerapkan teknik agregasi spasial kisi segi enam H3 (*Uber H3 Hexagonal Hierarchical Spatial Index*) untuk anonimisasi densitas massa warga.
- **Topik Teori Utama**: Geodesi spasial sistem proyeksi WGS 84, indeks spasial R-Tree dan H3, algoritma komputasi geometri titik dalam poligon (*Point-in-Polygon* / PiP), dan regulasi perlindungan data pribadi (UU PDP Indonesia / GDPR) pada telemetri ruang publik.
- **Landasan Matematis (KaTeX)**:
  - Formula Haversine jarak lengkung bumi dua koordinat lintang/bujur:
    $$
    d = 2 R \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)
    $$
    di mana $R = 6371\text{ km}$, $\phi$ adalah lintang, dan $\lambda$ adalah bujur dalam radian.
- **Worked Numerical Example**: Menghitung jarak geodesic antara simpul sensor kualitas udara di ITERA ($-5{,}3582^\circ\text{S}, 105{,}3145^\circ\text{E}$) dan stasiun BMKG terdekat ($-5{,}4012^\circ\text{S}, 105{,}2581^\circ\text{E}$), serta evaluasi latensi transmisi propagasi nirkabel.
- **Eksperimen Komputasi**: Modul Python query spasial PostGIS/GeoPandas yang memproses aliran event telemetri truk sampah kota dan menerbitkan peringatan jika keluar dari koridor geofence yang ditentukan.
- **Deliverables & Asesmen**: Peta visualisasi geospasial real-time dan modul deteksi pelanggaran geofencing terverifikasi.
- **Rujukan Primer**: Open Geospatial Consortium (OGC), *GeoJSON Format Specification (IETF RFC 7946)*; ISO 19125-1 (Geographic information — Simple feature access).

### Modul E06: Capstone — City-Scale Multi-Tenant IoT Telecommunications & Environmental Platform
- **Kode & Judul**: `E06 — Capstone: City-Scale Multi-Tenant IoT Telecommunications & Environmental Platform`
- **Kedalaman Akademik**: **L4: Research Preparation**
- **Prasyarat Kurikulum Inti**: Seluruh modul E01–E05, Chapter 30, Chapter 40.
- **Spesifikasi & Rincian**: Dijabarkan secara mendalam pada Seksi 7 (Capstone Design).

---

## 7. Rekomendasi Urutan Implementasi & Analisis Feasibility

Berdasarkan audit dependensi teknologi, ketersediaan toolchain simulasi perangkat lunak (Python, Node.js, C/C++), dan kesiapan infrastruktur laboratorium:

1. **Prioritas 1: Track B (Industrial IoT & Predictive Maintenance)**
   - *Justifikasi*: Melanjutkan secara linier Chapter 33 (Modbus/OPC UA), Chapter 35 (TinyML), dan Chapter 38 (Fault Injection). Ekosistem Python (`pymodbus`, `opcua-asyncio`, `scipy.signal`) sangat matang dan reproducible 100% tanpa hardware fisik berbayar.
2. **Prioritas 2: Track D (AIoT & Edge Intelligence)**
   - *Justifikasi*: Melanjutkan Chapter 35 (TinyML INT8) dan Chapter 36 (Digital Twin). Fokus pada pengolahan sinyal diskrit, kompresi QAT, dan Extended Kalman Filter yang memiliki nilai akademik dan riset sangat tinggi bagi mahasiswa teknik elektro & informatika.
3. **Prioritas 3: Track C (Smart Agriculture & Environmental Monitoring)**
   - *Justifikasi*: Memperdalam Chapter 07, 18, 19, dan 31. Relevan dengan konteks institusi ITERA di Sumatera (perkebunan, hidrologi, smart farming). Model matematis FAO-56 dan propagasi kanopi Weissberger sangat aplikatif.
4. **Prioritas 4: Track A (Smart Home & Building Automation)**
   - *Justifikasi*: Mengembangkan Chapter 34 (Matter/Thread) dan Chapter 28 (Security). Memerlukan pemodelan emulasi jaringan IPv6 Thread border router yang cukup kompleks namun sangat relevan untuk industri otomasi modern.
5. **Prioritas 5: Track E (IoT for Telecommunications & Smart Cities)**
   - *Justifikasi*: Merangkum seluruh arsitektur jaringan skala besar (Chapter 11, 18, 37, 39). Sangat tepat bagi mahasiswa Teknik Telekomunikasi; membutuhkan pemodelan spasial PostGIS dan simulasi antrean kontensi data masif.

