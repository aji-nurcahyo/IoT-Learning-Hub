# Rancangan Capstone 5 Jalur Peminatan
## IoT Learning Hub — Phase 6A: Specialization Capstone Architecture & Acceptance Criteria

Dokumen ini memuat spesifikasi rekayasa menyeluruh (*System Engineering Requirements Specification*) untuk 5 proyek akhir peminatan (*Specialization Capstones*): **A06**, **B06**, **C06**, **D06**, dan **E06**.

- **Proyek**: Internet of Things Learning Hub (*From Connected Devices to Intelligent Systems*)
- **Pengembang & Kurator**: Aji Pamungkas Tri Nurcahyo (Institut Teknologi Sumatera - ITERA)
- **Kebijakan Anti-Slop**: Permanent Active (Mode: **DURING**)
- **Fase**: Phase 6A — Specialization Architecture & Curriculum Design
- **Tanggal Rilis**: 18 November 2026

---

## 1. Capstone Track A (A06): Autonomous Micro-Climate & Demand-Response Building Controller

### 1.1 Engineering Problem Statement
Gedung komersial modern menghadapi konflik antara kenyamanan termal/kualitas udara penghuni (ASHRAE 62.1) dan biaya penalti lonjakan energi listrik akibat pemakaian pendingin udara (HVAC) yang tidak sinkron. Diperlukan pengontrol iklim mikro terdistribusi yang mampu mengelola zonasi ruangan secara mandiri (*local-first resilience*) berbasis protokol Matter/Thread, melakukan optimasi pemotongan beban puncak (*peak-shaving*), serta menjamin interlock keselamatan evakuasi darurat tanpa ketergantungan pada koneksi internet cloud.

### 1.2 Persyaratan Fungsional (FR)
- **FR-01**: Mengintegrasikan pembacaan data multi-sensor lingkungan (Suhu, RH, $\text{CO}_2$ NDIR, dan kehadiran radar mmWave) per zona ruangan dengan periode pembaruan $\le 2\text{ detik}$.
- **FR-02**: Mengimplementasikan kendali Demand-Controlled Ventilation (DCV) dengan histeresis deadband dinamis untuk menjaga konsentrasi $\text{CO}_2 < 800\text{ ppm}$.
- **FR-03**: Menerima dan mengeksekusi perintah kluster Matter (On/Off dan Level Control) melalui jaringan mesh Thread IPv6 lokal.
- **FR-04**: Menjalankan algoritma pemangkasan beban listrik bertingkat saat daya sesaat gedung mendekati batas daya kontrak $P_{\text{contract}}$.
- **FR-05**: Mengaktifkan interlock keselamatan perangkat keras saat sinyal alarm kebakaran (FAS dry-contact) terpicu: membuka seluruh pintu akses dan menghentikan kipas sirkulasi udara segar seketika.

### 1.3 Persyaratan Non-Fungsional (NFR)
- **NFR-01 (Kemandirian Lokal)**: Sistem wajib mempertahankan kendali iklim mikro dan keselamatan $100\%$ berjalan normal saat koneksi WAN internet terputus total.
- **NFR-02 (Latensi Respon)**: Waktu tanggap sejak alarm darurat terpicu hingga eksekusi relay pemutus interlock wajib $\le 100\text{ ms}$.
- **NFR-03 (Efisiensi Energi)**: Konsumsi energi pendingin udara berkurang minimal $15\%$ dibanding kendali termostat berbasis jadwal statis.

### 1.4 Model Matematika / Analitis
Model keseimbangan daya semu dan pemangkasan beban puncak:
$$
S_{\text{total}} = \sqrt{\left( \sum_{i=1}^{M} P_i \right)^2 + \left( \sum_{i=1}^{M} Q_i \right)^2}
$$
Algoritma pelepasan beban prioritaskan tier beban non-kritis ($k \in \text{Tier 3}$):
$$
\text{If } S_{\text{total}} > S_{\text{threshold}} \implies \text{ShedLoad}\left( \arg \max_{k \in \text{Tier 3}} P_k \right)
$$

### 1.5 Matriks Skenario Uji Penerimaan Sistem (SATC Matrix)

| Kode SATC | Nama Skenario Uji | Kondisi Masukan & Stimulus | Hasil yang Diharapkan | Kriteria Lulus (Pass Criteria) |
|---|---|---|---|---|
| **SATC-A01** | IAQ Closed-Loop Ventilation | Injeksi konsentrasi $\text{CO}_2$ meningkat dari 600 ppm ke 1100 ppm saat terdeteksi okupansi radar mmWave. | Katup ventilasi udara segar membuka proporsional ($100\%$), laju pertukaran udara meningkat, $\text{CO}_2$ kembali $< 800\text{ ppm}$. | Waktu respon kendali $\le 5\text{ detik}$; ketiadaan osilasi buka-tutup katup (*chattering*). |
| **SATC-A02** | Local Thread Mesh Robustness | Putuskan koneksi antarmuka WAN / Ethernet pada Border Router. | Komunikasi kendali antar-node Thread tetap berjalan normal; perintah sakelar Matter lokal dieksekusi seketika. | Packet Delivery Ratio lokal $100\%$; latensi transmisi perintah $< 50\text{ ms}$. |
| **SATC-A03** | Automated Peak-Shaving Trigger | Beban daya aktif total dinaikkan hingga mencapai $92\%$ dari batas trafo gedung ($P_{\text{load}} = 92\text{ kW}$, batas $100\text{ kW}$). | Sistem otomatis menonaktifkan unit pendingin zona koridor dan menurunkan setpoint chiller sekunder. | Daya total turun kembali ke $< 85\text{ kW}$ dalam waktu $\le 3\text{ detik}$; tidak ada trip MCB utama. |
| **SATC-A04** | Life-Safety Interlock Verification | Simulasikan putusnya loop pengawas EOL atau penekanan tombol manual call point darurat FAS. | Seluruh relay pengunci pintu magnetik kehilangan daya (*fail-safe unlocked*); sistem sirkulasi udara mati. | Transisi status terjadi dalam waktu $< 80\text{ ms}$; log darurat tercatat di memori non-volatile RTC. |

### 1.6 Rubrik Penilaian Capstone (Total 100 Poin)
1. **Arsitektur Sistem & Interoperabilitas Matter/Thread** (25 poin): Ketepatan pemetaan cluster Matter, topologi IPv6 Thread mesh, dan ketahanan kendali lokal.
2. **Kinerja Algoritma Pengendalian IAQ & Energi** (25 poin): Akurasi respon loop tertutup ventilasi $\text{CO}_2$, kestabilan histeresis, dan efektivitas algoritma peak-shaving.
3. **Keandalan & Interlock Keselamatan Darurat** (25 poin): Implementasi sirkuit loop terawasi fail-safe, determinisme waktu tanggap interlock, dan mitigasi bahaya kebakaran.
4. **Kualitas Kode, Dokumentasi & Reproduksibilitas** (25 poin): Kode simulasi modular, lulus 100% SATC, skematik jelas, dan rujukan standar ASHRAE/NFPA lengkap.

---

## 2. Capstone Track B (B06): Edge Predictive Maintenance System with High-Speed Sampling

### 2.1 Engineering Problem Statement
Kegagalan mekanis katastropik pada mesin rotasi industri (motor induksi, pompa sentrifugal, turbin angin) menimbulkan kerugian jutaan dolar akibat penghentian mendadak lini produksi (*unscheduled downtime*). Metode pemantauan berkala bulanan sering kali terlambat mendeteksi inisiasi keretakan mikro pada elemen gelinding bantalan (*bearing flaking*). Diperlukan sistem Edge IIoT cerdas yang mampu mengakuisisi sinyal akselerasi getaran pada laju sampling tinggi ($f_s \ge 10\text{ kHz}$), mengekstraksi fitur statistik domain waktu dan frekuensi selubung secara deterministik, serta memetakan kondisi kesehatan aset ke dalam model informasi OPC UA standar industri.

### 2.2 Persyaratan Fungsional (FR)
- **FR-01**: Mengakuisisi sinyal getaran multi-sumbu pada laju sampling minimum $f_s = 10\text{ kHz}$ secara bebas jitter menggunakan buffer DMA (*Direct Memory Access*).
- **FR-02**: Menghitung secara real-time metrik getaran standar ISO 20816: RMS kecepatan getaran ($V_{\text{RMS}}$), Peak-to-Peak akselerasi, dan Kurtosis sinyal.
- **FR-03**: Menjalankan algoritma Transformasi Hilbert untuk demodulasi selubung sinyal getaran dan menghitung spektrum FFT frekuensi cacat bantalan (BPFO, BPFI).
- **FR-04**: Mengklasifikasikan kondisi operasional mesin ke dalam 4 zona keparahan getaran ISO: Zona A (Baik Sekali), Zona B (Layak Operasi), Zona C (Peringatan / Dibatasi), dan Zona D (Bahaya Kritis).
- **FR-05**: Memublikasikan seluruh status metrik dan indeks kesehatan bantalan ke server OPC UA terstruktur yang dapat diakses SCADA level 2/3.

### 2.3 Persyaratan Non-Fungsional (NFR)
- **NFR-01 (Determinisme Eksekusi)**: Siklus pemrosesan blok data $2048$ sampel (ekstraksi fitur + FFT + klasifikasi) wajib selesai dalam waktu $\le 100\text{ ms}$ tanpa kehilangan sampel (*zero buffer overflow*).
- **NFR-02 (Akurasi Spektral)**: Resolusi frekuensi FFT wajib $\Delta f \le 2{,}5\text{ Hz}$ untuk membedakan komponen harmonik poros dengan frekuensi slip motor.
- **NFR-03 (Ketahanan Industri)**: Sistem wajib mampu beroperasi pada bus Modbus RS-485 / Industrial Ethernet dengan isolasi galvanik $1{,}5\text{ kV}$.

### 2.4 Model Matematika / Analitis
Pembentukan sinyal analitik kompleks melalui Transformasi Hilbert untuk ekstraksi selubung amplitudo $A(t)$:
$$
\tilde{x}(t) = x(t) + j \cdot \mathcal{H}\{x(t)\} = A(t) e^{j \phi(t)}
$$
$$
A(t) = \sqrt{x^2(t) + (\mathcal{H}\{x(t)\})^2}
$$
Spektrum selubung diperoleh dengan menerapkan FFT pada $A(t)$:
$$
S_{\text{env}}(f) = |\mathcal{F}\{A(t) - \bar{A}\}|
$$

### 2.5 Matriks Skenario Uji Penerimaan Sistem (SATC Matrix)

| Kode SATC | Nama Skenario Uji | Kondisi Masukan & Stimulus | Hasil yang Diharapkan | Kriteria Lulus (Pass Criteria) |
|---|---|---|---|---|
| **SATC-B01** | High-Rate Acquisition & DMA Integrity | Aliran data getaran disimulasikan kontinu pada $f_s = 10.240\text{ Hz}$ selama $60\text{ detik}$ ($614.400$ sampel). | Buffer ganda DMA bergantian mengisi tanpa terjadi buffer overrun atau data terpotong. | Rasio kehilangan sampel (*Sample Loss Rate*) $= 0{,}00\%$; latensi buffer swap $< 10\,\mu\text{s}$. |
| **SATC-B02** | Incipient Bearing Fault Detection | Injeksi sinyal benturan mikro tersembunyi pada frekuensi karakteristik cincin luar bantalan $\text{BPFO} = 107{,}5\text{ Hz}$ beramplitudo rendah (tertutup derau putih Gauss $\text{SNR} = -5\text{ dB}$). | Nilai Kurtosis melonjak ($> 4{,}5$) dan analisis spektrum selubung Hilbert mendeteksi puncak dominan pada $107{,}5\text{ Hz} \pm 1\text{ Hz}$. | Deteksi puncak spektral BPFO memiliki margin $\ge 6\text{ dB}$ di atas lantai derau spektrum selubung. |
| **SATC-B03** | ISO 20816 Severity Classification | Stimulus getaran ditingkatkan hingga $V_{\text{RMS}} = 7{,}2\text{ mm/s}$ (melebihi ambang batas Kelas II Zona C). | Mesin status otomatis beralih ke status \`SEVERITY_ZONA_C\` dan memicu alarm peringatan pemeliharaan. | Klasifikasi zona sesuai tabel ISO 20816 dalam waktu $\le 1$ siklus pemrosesan blok. |
| **SATC-B04** | OPC UA NodeSet Synchronization | Klien OPC UA membaca node variabel \`VibrationRMS\`, \`BearingHealthIndex\`, dan berlangganan event \`MachineAlarmEvent\`. | Nilai register dan status alarm diperbarui secara sinkron pada pohon alamat OPC UA tanpa jeda. | Nilai variabel OPC UA identik dengan keluaran perhitungan edge; event alarm diterima klien $\le 50\text{ ms}$. |

### 2.6 Rubrik Penilaian Capstone (Total 100 Poin)
1. **Akuisisi Sinyal & Kinerja Pemrosesan Digital** (25 poin): Integritas sampling frekuensi tinggi, efisiensi alokasi memori buffer DMA, dan ketepatan perhitungan FFT/Kurtosis.
2. **Keandalan Deteksi Anomali Cacat Bantalan** (25 poin): Ketepatan implementasi Transformasi Hilbert, identifikasi puncak frekuensi cacat mekanis, dan ketahanan terhadap noise.
3. **Kepatuhan Standar Industri & Integrasi OPC UA** (25 poin): Kesesuaian klasifikasi terhadap ISO 20816, arsitektur model informasi OPC UA, dan segmentasi keamanan OT/IT.
4. **Verifikasi Eksperimental & Reproduksibilitas** (25 poin): Kelulusan 100% SATC, analisis profil eksekusi waktu komputasi, dan penyusunan technical report yang komprehensif.

---

## 3. Capstone Track C (C06): Autonomous LoRaWAN Agricultural Microclimate Network

### 3.1 Engineering Problem Statement
Lahan pertanian dan perkebunan terpencil sering kali tidak memiliki suplai listrik jaringan kabel dan berada di luar jangkauan sinyal seluler komersial. Petani menghadapi risiko kekeringan tanaman atau pemborosan air tanah akibat penjadwalan irigasi yang bersifat tebakan. Diperlukan jaringan stasiun mikroklimat otonom berdaya ultra-rendah yang mampu beroperasi selama bertahun-tahun hanya mengandalkan pemanen energi surya mikro, mentransmisikan data kondisi tanah dan cuaca melalui radio LoRaWAN jarak jauh melintasi tajuk pepohonan lebat, serta menghitung kebutuhan air tanaman presisi berbasis formula FAO-56 Penman-Monteith secara otomatis.

### 3.2 Persyaratan Fungsional (FR)
- **FR-01**: Mengumpulkan data sensor in-situ multi-titik (Kelembaban volumetrik tanah VWC, suhu tanah, suhu udara, kelembaban udara RH, radiasi matahari, dan kecepatan angin) setiap interval $15\text{ menit}$.
- **FR-02**: Menerapkan algoritma kompensasi drift suhu dan kalibrasi dua titik in-situ pada pembacaan permitivitas sensor tanah.
- **FR-03**: Mengemas data ke dalam payload biner terkompresi ringkas ($\le 16\text{ byte}$) dan mentransmisikannya ke Gateway LoRaWAN melalui kanal nirkabel sub-GHz ($920\text{ MHz}$).
- **FR-04**: Mengelola siklus tidur deep sleep mikrokontroler dengan konsumsi arus statis $\le 10\,\mu\text{A}$ di antara siklus sampling.
- **FR-05**: Menghitung laju evapotranspirasi acuan harian ($\text{ET}_0$) di sisi gateway/platform dan menghasilkan rekomendasi durasi irigasi defisit terkendali.

### 3.3 Persyaratan Non-Fungsional (NFR)
- **NFR-01 (Otonomi Energi Mandiri)**: Sistem catu daya panel surya dan superkapasitor/LiFePO4 wajib menjamin operasional kontinu minimum 7 hari tanpa penyinaran matahari (*7 Days of Autonomy*).
- **NFR-02 (Jangkauan Transmisi Nirkabel)**: Tautan radio LoRaWAN wajib mampu menembus jarak minimum $3\text{ km}$ melintasi kanopi perkebunan dengan Packet Delivery Ratio $\ge 95\%$.
- **NFR-03 (Ketahanan Enclosure)**: Unit stasiun sensor lapangan wajib memiliki proteksi fisik bersertifikasi IP67 dan tahan terhadap kelembaban jenuh $100\%$.

### 3.4 Model Matematika / Analitis
Persamaan kesetimbangan neraca air tanah (*Soil Water Depletion* $D_{r,i}$) harian:
$$
D_{r,i} = D_{r,i-1} - (P_i - \text{RO}_i) - I_i - \text{CR}_i + \text{ET}_{c,i} + \text{DP}_i
$$
di mana $\text{ET}_{c,i} = K_c \cdot \text{ET}_{0,i}$ adalah evapotranspirasi tanaman, $P$ curah hujan, $I$ irigasi, dan $\text{RO}$ limpasan permukaan.
Trigger irigasi aktif saat penipisan air tanah melampaui ambang batas yang diizinkan (*Management Allowed Depletion*):
$$
\text{If } D_{r,i} > \text{RAW} = p_{\text{tab}} \cdot \text{TAW} \implies \text{ActivateIrrigation}
$$

### 3.5 Matriks Skenario Uji Penerimaan Sistem (SATC Matrix)

| Kode SATC | Nama Skenario Uji | Kondisi Masukan & Stimulus | Hasil yang Diharapkan | Kriteria Lulus (Pass Criteria) |
|---|---|---|---|---|
| **SATC-C01** | Soil Calibration & Thermal Stability | Sensor tanah diuji pada variasi temperatur dari $20^\circ\text{C}$ hingga $42^\circ\text{C}$ pada kadar air konstan. | Pembacaan kadar air terkompensasi tetap stabil tanpa deviasi drift melebihi batas toleransi. | Galat pengukuran kelembaban tanah terkompensasi suhu $|\Delta \theta| \le 1{,}5\%\text{ VWC}$. |
| **SATC-C02** | Canopy Link Budget Verification | Transmisi paket LoRaWAN melintasi simulasi redaman tajuk pohon setebal $50\text{ meter}$ ($L_{\text{veg}} \approx 18\text{ dB}$) pada jarak $3{,}5\text{ km}$ ($f = 920\text{ MHz}$, SF10). | Paket diterima oleh gateway dengan margin sinyal $\text{SNR} > -15\text{ dB}$ dan RSSI di atas sensitivitas penerima. | Packet Delivery Ratio (PDR) $\ge 95\%$ dari 200 paket uji berurutan. |
| **SATC-C03** | Energy Harvesting & Autonomy Stress | Profil suplai daya disimulasikan dalam kondisi mendung ekstrem ($0\text{ mW}$ daya masuk surya) selama 168 jam kontinu. | Node tetap beroperasi normal dengan menurunkan frekuensi sampling secara adaptif saat tegangan superkapasitor drop. | Tidak terjadi crash sistem (*no brownout reset*); tegangan baterai/superkapasitor tetap $> V_{\text{min}}$. |
| **SATC-C04** | FAO-56 Precision Irrigation Decision | Injeksi telemetri iklim mikro terik ($R_n = 22\text{ MJ/m}^2$, suhu $32^\circ\text{C}$, angin $2{,}5\text{ m/s}$) dan kadar air tanah menyusut ke titik kritis MAD. | Modul analitik menghitung $\text{ET}_0 = 5{,}8\text{ mm/hari}$ dan menerbitkan perintah downlink irigasi dengan volume tepat. | Volume irigasi tepat mengembalikan kelembaban ke kapasitas lapang tanpa terjadi limpasan air (*deep percolation* $= 0$). |

### 3.6 Rubrik Penilaian Capstone (Total 100 Poin)
1. **Desain Catu Daya Mandiri Energi & Low-Power** (25 poin): Ketepatan dimensi panel surya/superkapasitor, profil arus deep sleep terukur, dan algoritma adaptif otonomi.
2. **Kinerja Link Radio LoRaWAN & Redaman Tajuk** (25 poin): Akurasi perhitungan link budget, optimasi parameter radio (SF/BW), dan ketahanan transmisi jarak jauh.
3. **Analitika Evapotranspirasi FAO-56 & Irigasi Presisi** (25 poin): Implementasi persamaan FAO-56, akurasi neraca air tanah, dan efisiensi air aktuasi irigasi.
4. **Reproduksibilitas, Pengujian Lapangan & Dokumentasi** (25 poin): Kelulusan 100% skenario SATC, kejelasan model kalibrasi sensor tanah, dan penyajian laporan teknik standar WMO.

---

## 4. Capstone Track D (D06): Real-Time Multimodal Edge Vision & Acoustic Anomaly Detection System

### 4.1 Engineering Problem Statement
Deteksi anomali pada peralatan manufaktur atau robotika otonom sering kali tidak cukup hanya mengandalkan satu modalitas sensor. Anomali akustik (suara desis kebocoran gas bertekanan) mendahului getaran mekanis, sementara perubahan visual permukaan (keausan fisik atau asap mikro) memerlukan analisis spasial. Namun, mentransmisikan video dan audio mentah berkecepatan tinggi ke server cloud menimbulkan latensi jaringan ratusan milidetik dan menghabiskan bandwidth jaringan pabrik. Diperlukan sistem Edge AI terpadu yang mampu menjalankan fusi multimodal (akustik ultrasonik dan visual beresolusi rendah) langsung di dalam mikrokontroler/Edge NPU menggunakan model TinyML terkuantisasi INT8 dengan latensi inferensi sub-detik.

### 4.2 Persyaratan Fungsional (FR)
- **FR-01**: Mengakuisisi aliran sinyal mikrofon PDM/I2S pada frekuensi sampling $16\text{ kHz}$ dan frame citra visual grayscale $96 \times 96$ piksel secara sinkron.
- **FR-02**: Mengekstraksi fitur spektrogram Mel (MFCC 10 koefisien) dari sinyal audio secara streaming dalam memori penyangga fixed-point.
- **FR-03**: Menjalankan inferensi model jaringan saraf konvolusi terkuantisasi INT8 penuh (weights dan activations) menggunakan runtime TFLite Micro.
- **FR-04**: Menggabungkan probabilitas anomali audio dan visual menggunakan algoritma Bayesian Late-Fusion untuk menghasilkan indeks keparahan komposit ($I_{\text{composite}}$).
- **FR-05**: Memicu sinyal aktuasi keselamatan perangkat keras (pemutus relay darurat) saat indeks komposit anomali melebihi ambang batas keyakinan $90\%$ selama 3 frame berurutan.

### 4.3 Persyaratan Non-Fungsional (NFR)
- **NFR-01 (Latensi Inferensi Sub-Detik)**: Total waktu eksekusi end-to-end (akuisisi + pra-pemrosesan fitur + inferensi INT8 ganda + fusi) wajib $\le 250\text{ ms}$ pada clock inti prosesor $240\text{ MHz}$.
- **NFR-02 (Jejak Memori SRAM Terbatas)**: Total alokasi memori dinamis (*Tensor Arena + DMA buffers*) tidak boleh melebihi $256\text{ KiB}$ SRAM internal mikrokontroler.
- **NFR-03 (Ketahanan Terhadap False-Alarm)**: Tingkat alarm palsu (*False Positive Rate* / FPR) sistem wajib $\le 1{,}0\%$ pada kondisi derau lingkungan pabrik normal.

### 4.4 Model Matematika / Analitis
Formulasi Bayesian Late-Fusion untuk menggabungkan skor probabilitas posterior modalitas visual ($P_v = P(\text{Anomaly}|x_{\text{vision}})$) dan modalitas akustik ($P_a = P(\text{Anomaly}|x_{\text{audio}})$) dengan asumsi independensi bersyarat:
$$
P(\text{Anomaly}|x_v, x_a) = \frac{P_v \cdot P_a}{P_v \cdot P_a + (1 - P_v)(1 - P_a)}
$$
Model kuantisasi perkalian fixed-point INT8 tanpa FPU:
$$
q_y = \text{SRound}\left( M_0 \cdot 2^{-n} \sum_{i} (q_{w,i} - Z_w)(q_{x,i} - Z_x) \right) + Z_y
$$

### 4.5 Matriks Skenario Uji Penerimaan Sistem (SATC Matrix)

| Kode SATC | Nama Skenario Uji | Kondisi Masukan & Stimulus | Hasil yang Diharapkan | Kriteria Lulus (Pass Criteria) |
|---|---|---|---|---|
| **SATC-D01** | Fixed-Point Audio Feature Extraction | Sinyal audio anomali gesekan logam ($16\text{ kHz}$) diproses melalui ekstraktor MFCC fixed-point integer $Q15$. | Nilai koefisien MFCC integer identik dengan perhitungan acuan float32 dengan galat kuantisasi terabaikan. | Mean Absolute Error (MAE) koefisien MFCC $|\text{MAE}| \le 0{,}02$; waktu komputasi per jendela $\le 15\text{ ms}$. |
| **SATC-D02** | INT8 Model Memory Arena Boundary | Runtime TFLite Micro menginisialisasi model CNN visual dan audio di dalam blok memori tensor statis teralokasi. | Model berhasil dialokasikan di dalam Tensor Arena tanpa memicu alokasi heap runtime atau overflow stack. | Pemakaian memori SRAM total $\le 256\text{ KiB}$; heap bebas tidak berkurang saat inferensi berjalan (*zero heap churn*). |
| **SATC-D03** | Multimodal Bayesian Fusion Accuracy | Stimulus audio anomali diberikan bersamaan dengan citra visual normal (misalnya kebocoran gas tanpa perubahan visual). | Fusi Bayesian secara adaptif menaikkan keyakinan komposit anomali ke tingkat menengah ($72\%$), menghindari miss-detection. | Indeks anomali mencerminkan kontribusi modalitas secara probabilistik tanpa mengalami dominasi skewing. |
| **SATC-D04** | End-to-End Latency & Actuation | Pemicuan anomali ganda (percikan api visual + suara desis impak frekuensi tinggi serentak). | Sistem mendeteksi anomali kritis ($P_{\text{composite}} > 95\%$) dan mengaktifkan pin aktuasi keselamatan seketika. | Waktu total sejak input sensor tiba hingga pin sinyal interlock aktif $\le 250\text{ ms}$. |

### 4.6 Rubrik Penilaian Capstone (Total 100 Poin)
1. **Optimalisasi Arsitektur & Kuantisasi Model TinyML** (25 poin): Ketepatan penerapan kuantisasi INT8 penuh, efisiensi komputasi fixed-point, dan pemeliharaan akurasi model.
2. **Kinerja Pipeline Sinyal & Fusi Bayesian** (25 poin): Kualitas implementasi pra-pemrosesan streaming, ketepatan formula fusi Bayesian, dan mitigasi false-alarm.
3. **Kepatuhan Batasan Memori & Latensi Real-Time** (25 poin): Pembuktian batas memori SRAM $\le 256\text{ KiB}$, determinisme latensi $\le 250\text{ ms}$, dan stabilitas jangka panjang.
4. **Validasi Eksperimental & Reproduksibilitas** (25 poin): Kelulusan 100% skenario SATC, profil komparasi model FP32 vs INT8, dan kode sumber berstandar MISRA C/Python clean code.

---

## 5. Capstone Track E (E06): City-Scale Multi-Tenant IoT Telecommunications & Environmental Platform

### 5.1 Engineering Problem Statement
Pemerintah kota metropolitan mengelola ribuan aset publik terdesentralisasi: lampu penerangan jalan pintar (PJU), sensor kualitas udara distrik, meteran air utilitas publik, dan pemantau tinggi muka air kanal pencegah banjir. Mengoperasikan infrastruktur telekomunikasi independen untuk masing-masing dinas menimbulkan pemborosan anggaran yang masif. Diperlukan platform telekomunikasi IoT kota multi-tenant skala besar yang mampu menangani konsentrasi paket telemetri masif ($\ge 10.000\text{ paket/detik}$), mengelola isolasi data antar-dinas secara aman berbasis model ontologi perkotaan standar (FIWARE NGSI-LD), menjamin Service Level Agreement (SLA) keterlambatan paket telemetri kritis (banjir) di atas jaringan LPWAN/seluler, serta mengamankan privasi spasial warga melalui geofencing dan agregasi spasial H3.

### 5.2 Persyaratan Fungsional (FR)
- **FR-01**: Mengingest aliran data telemetri dari 50.000 simpul perangkat heterogen terdistribusi (LoRaWAN, NB-IoT, dan Wi-Fi kota) dengan throughput puncak $\ge 10.000\text{ paket/detik}$.
- **FR-02**: Mengonversi dan memvalidasi payload telemetri mentah ke dalam format standar entitas kota cerdas FIWARE NGSI-LD (*Smart Data Models*).
- **FR-03**: Menerapkan isolasi multi-tenant yang ketat (Dinas Kebersihan, Dinas PUPR, Dinas Perhubungan) menggunakan token otorisasi kriptografis dan Access Control List (ACL).
- **FR-04**: Mengklasifikasikan dan memprioritaskan antrean paket darurat (misalnya ambang batas air banjir kanal meluap) melintasi broker pesan terdistribusi (*Priority Queueing*).
- **FR-05**: Menjalankan mesin pemrosesan spasial real-time: pengecekan geofencing armada kendaraan dinas dan agregasi densitas sensor kualitas udara pada kisi heksagonal Uber H3 resolusi 8.

### 5.3 Persyaratan Non-Fungsional (NFR)
- **NFR-01 (Throughput & Latensi P99)**: Latensi transit telemetri end-to-end persentil ke-99 ($P_{99}$) wajib $\le 500\text{ ms}$ pada beban kerja $10.000\text{ paket/detik}$.
- **NFR-02 (Ketersediaan Layanan Komposit)**: Ketersediaan kluster broker ingestion dan database deret waktu spasial wajib memenuhi SLA Four-Nines ($A \ge 99{,}99\%$).
- **NFR-03 (Privasi Spasial Publik)**: Seluruh data telemetri yang diekspos ke portal data terbuka publik wajib dianonimkan melalui generalisasi spasial H3 tanpa mengekspos koordinat presisi perangkat individu.

### 5.4 Model Matematika / Analitis
Model antrean prioritas $M/G/1$ Non-Preemptive untuk menjamin SLA latensi paket darurat prioritas tinggi ($p=1$) di atas paket telemetri reguler ($p=2$):
Waktu tunggu rata-rata paket prioritas tinggi $W_1$:
$$
W_1 = \frac{W_0}{1 - \rho_1}
$$
di mana waktu tunda sisa layanan $W_0 = \frac{1}{2} \sum_{i=1}^{2} \lambda_i \overline{X_i^2}$, $\lambda_i$ adalah laju kedatangan kelas $i$, dan $\rho_1 = \lambda_1 \overline{X_1}$ adalah utilitas kelas prioritas.
Kompensasi jaminan latensi paket darurat membuktikan $W_1 \ll W_2$.

### 5.5 Matriks Skenario Uji Penerimaan Sistem (SATC Matrix)

| Kode SATC | Nama Skenario Uji | Kondisi Masukan & Stimulus | Hasil yang Diharapkan | Kriteria Lulus (Pass Criteria) |
|---|---|---|---|---|
| **SATC-E01** | Massive Telemetry Ingestion Stress | Beban lalu lintas disimulasikan melonjak hingga $12.000\text{ paket/detik}$ selama 10 menit terus-menerus. | Kluster ingest buffer mendistribusikan beban secara merata via Consistent Hashing tanpa kehilangan paket. | Drop rate paket $= 0{,}00\%$; utilisasi memori kluster broker stabil tanpa memory leak. |
| **SATC-E02** | Priority Emergency Queueing Under Load | Saat sistem berada di bawah beban puncak ($10.000\text{ req/s}$), diinjeksikan paket peringatan banjir kritis secara mendadak. | Paket darurat langsung diproses di antrean prioritas tertinggi mendahului paket reguler. | Latensi end-to-end paket peringatan banjir $\le 80\text{ ms}$ (memenuhi SLA darurat bencana). |
| **SATC-E03** | Multi-Tenant Data Isolation Security | Klien yang diautentikasi dengan token kredensial Dinas Kebersihan mencoba membaca data sensor air Dinas PUPR via NGSI-LD API. | Permintaan akses ditolak seketika dengan status HTTP \`403 Forbidden\` dan dicatat pada audit log keamanan. | Ketiadaan celah kebocoran data lintas tenant (*Zero Cross-Tenant Leakage*). |
| **SATC-E04** | Spatial Geofencing & H3 Privacy Masking | Aliran koordinat GPS kendaraan operasional diuji melintasi batas poligon geofence kota; data diekspor ke open API publik. | Pelanggaran batas memicu alert seketika; API publik menyajikan agregasi densitas heksagonal H3 tanpa koordinat raw. | Waktu deteksi pelanggaran batas geofence $\le 100\text{ ms}$; privasi spasial individu terlindungi secara matematis. |

### 5.6 Rubrik Penilaian Capstone (Total 100 Poin)
1. **Arsitektur Skalabilitas & Ingestion Throughput Tinggi** (25 poin): Ketepatan perancangan kluster broker terdistribusi, sharding partisi data, dan ketahanan terhadap lonjakan data masif.
2. **Jaminan Kualitas Layanan (SLA) & Antrean Prioritas** (25 poin): Implementasi antrean prioritas $M/G/1$, evaluasi latensi ekor $P_{99}$, dan determinisme respon darurat.
3. **Kepatuhan Standar Kota Cerdas & Tata Kelola Privasi** (25 poin): Kesesuaian model data FIWARE NGSI-LD, isolasi multi-tenant, dan agregasi spasial anonimitas H3.
4. **Verifikasi Kinerja, Otomasi Pengujian & Dokumentasi** (25 poin): Kelulusan 100% skenario SATC, visualisasi dashboard geospasial real-time, dan dokumentasi arsitektur sistem skala metropolitan.

