# Modul B01 — Industrial Automation Architecture, Purdue Model & OT/IT DMZ Security

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memetakan arsitektur piramida otomasi industri mengacu pada Model Referensi Purdue (PERA) dan standar ISA-95 dari Level 0 hingga Level 4.
2. Menganalisis batasan keamanan siber industri IEC 62443 berbasis konsep Zones and Conduits.
3. Merancang arsitektur Industrial Demilitarized Zone (IDMZ) dan konfigurasi proxy replikasi data yang mengisolasi jaringan kendali operasional (OT) dari jaringan korporat (IT).
4. Mengevaluasi risiko keamanan transmisi langsung paket kendali dari jaringan luar ke perangkat PLC dan fieldbus.

## Prasyarat
- Pemahaman dasar arsitektur IoT dan aliran data (Chapter 01 & Chapter 02).
- Fondasi jaringan komputer, subnetting, TCP/IP, dan port komunikasi (Chapter 11).
- Konsep dasar keamanan IoT, kriptografi TLS, dan matriks Access Control List (Chapter 28).

## Konsep dan teori

### 1. Arsitektur Otomasi Industri & Model Referensi Purdue (PERA / ISA-95)
Dalam lingkungan manufaktur modern, konvergensi antara *Operational Technology* (OT) dan *Information Technology* (IT) membutuhkan segmentasi yang ketat. Model Referensi Purdue membagi fasilitas industri ke dalam 5 tingkatan hierarki fungsional:

| Level Purdue | Nama Lapisan Fungsional | Perangkat & Sistem Khas | Karakteristik Waktu & Protokol |
|---|---|---|---|
| **Level 0** | *Physical Process / Field* | Sensor getaran, termokopel, motor induksi, katup solenoid | Kontinu fisik, sinyal analog 4–20 mA, 0–10 V |
| **Level 1** | *Basic Control* | Programmable Logic Controller (PLC), RTU, Drive (VFD) | Hard real-time (< 10 ms), Modbus RTU/TCP, PROFINET |
| **Level 2** | *Area Supervisory Control* | Supervisory Control and Data Acquisition (SCADA), HMI | Soft real-time (< 500 ms), OPC UA, Ethernet/IP |
| **Level 3** | *Manufacturing Operations* | Manufacturing Execution System (MES), Plant Historian | Batch & transaksi menit, Database SQL, MQTT |
| **Level 3.5** | **Industrial DMZ (IDMZ)** | Replicated Historian, Bastion Host, Remote Access Proxy | Firewall stateful, inspeksi paket, proksi dua arah |
| **Level 4** | *Enterprise Network* | Enterprise Resource Planning (ERP), Cloud Analytics | Asinkron web, HTTPS, REST API, SAP/Oracle |

### 2. Standar Keamanan IEC 62443: Zones & Conduits
Standar internasional IEC 62443 melarang topologi jaringan datar (*flat network*). Sebagai gantinya, aset dikelompokkan ke dalam **Zones** (kumpulan aset dengan kebutuhan tingkat keamanan Security Level yang sama). Komunikasi antar-zona hanya boleh berlangsung melalui saluran yang diawasi secara eksplisit yang disebut **Conduits**:

```
+-------------------------------------------------------------+
|              LEVEL 4: ENTERPRISE NETWORK (IT)               |
|            [ERP Server]       [Business Analysts]           |
+-------------------------------------------------------------+
                              |
                     === IDMZ CONDUIT === (HTTPS / SQL Replica)
                              v
+-------------------------------------------------------------+
|             LEVEL 3.5: INDUSTRIAL DMZ (IDMZ)                |
|      [Replicated Historian]        [OPC UA Edge Gateway]    |
+-------------------------------------------------------------+
                              |
                    === PLANT CONDUIT === (OPC UA / MQTT TLS)
                              v
+-------------------------------------------------------------+
|         LEVEL 3: MANUFACTURING OPERATIONS & MES (OT)        |
|             [Plant Historian]       [MES Master]            |
+-------------------------------------------------------------+
                              |
                    === CONTROL CONDUIT === (Modbus / PROFINET)
                              v
+-------------------------------------------------------------+
|         LEVEL 1 & 2: SUPERVISORY & PLC CONTROL (OT)         |
|             [SCADA Server] <-----> [PLC / RTU Node]         |
+-------------------------------------------------------------+
```

### 3. Landasan Matematis: Metrik Ketersediaan Zona & Pemodelan Penetrasi Keamanan (Mathematical Foundations)

Keandalan operasional sistem otomasi berantai dihitung melalui model ketersediaan seri:

1. **Ketersediaan Jalur Telemetri Bertingkat**:
   Jika jalur akuisisi data melewati $k$ lapisan subsistem independen dengan ketersediaan $A_i$:
   $$
   A_{\text{total}} = \prod_{i=1}^{k} A_i
   $$
   Jika Level 1 memiliki $A_1 = 0{,}999$, Level 2 $A_2 = 0{,}998$, Level 3 $A_3 = 0{,}995$, dan IDMZ gateway $A_{\text{idmz}} = 0{,}999$:
   $$
   A_{\text{total}} = 0{,}999 \times 0{,}998 \times 0{,}995 \times 0{,}999 \approx 0{,}9910 \quad (99{,}10\%)
   $$

2. **Kuantifikasi Reduksi Risiko Serangan Siber dengan IDMZ (Worked Example)**:
   Probabilitas keberhasilan serangan penetrasi siber dari jaringan luar $P_{\text{breach}}$ tanpa pembatas segmentasi dimodelkan sebagai peluang eksploitasi langsung $P_{\text{direct}} = 0{,}35$.
   Dengan menerapkan dua lapisan firewall stateful terpisah (External Firewall dengan resistansi pertahanan $R_{\text{ext}} = 0{,}90$ dan Internal Firewall dengan resistansi $R_{\text{int}} = 0{,}95$):
   $$
   P_{\text{breach, IDMZ}} = P_{\text{direct}} \times (1 - R_{\text{ext}}) \times (1 - R_{\text{int}})
   $$
   Substitusi nilai:
   $$
   P_{\text{breach, IDMZ}} = 0{,}35 \times (1 - 0{,}90) \times (1 - 0{,}95) = 0{,}35 \times 0{,}10 \times 0{,}05 = 0{,}00175 \quad (0{,}175\%)
   $$
   Penerapan arsitektur IDMZ memangkas probabilitas penetrasi ancaman hingga **200 kali lipat** dibanding jaringan tanpa demarkasi bertingkat.

## Latihan
1. **Analisis Segmentasi Purdue**: Jelaskan mengapa stasiun kerja operator HMI di Level 2 dilarang keras memiliki kartu antarmuka jaringan (NIC) ganda yang menghubungkannya langsung ke jaringan kantor Level 4!
2. **Kalkulasi Ketersediaan Gateway**: Sebuah pabrik menggunakan dua gateway IDMZ paralel (Active-Standby) masing-masing dengan availability $A = 0{,}99$. Hitung ketersediaan gabungan tier IDMZ tersebut!
3. **Audit Protokol Conduit**: Tinjau paket Modbus TCP yang dikirim dari alamat IP $192.168.10.50$ (Level 4 Enterprise) menuju $10.0.1.12$ (Level 1 PLC). Sebutkan dua pelanggaran aturan standar IEC 62443 yang terjadi!

## Tugas
Rancang dokumen spesifikasi zonasi keamanan jaringan otomasi industri (*Industrial Network Zoning Specification*) untuk pabrik perakitan otomotif:
1. Petakan seluruh aset (robot pengelasan, sensor getaran conveyor, PLC, SCADA, MES, dan ERP) ke dalam level Purdue yang benar.
2. Definisikan aturan tabel penyaringan paket (*firewall packet filtering rules*) pada Industrial DMZ, termasuk protokol, arah aliran data (*inbound/outbound*), dan nomor port TCP/UDP.
3. Lampirkan skrip simulasi Python atau diagram arsitektur conduit yang membuktikan bahwa perintah kendali kritis terisolasi dari jaringan eksternal.

## Ringkasan
- Model Referensi Purdue (PERA/ISA-95) dan IEC 62443 menyediakan kerangka kerja rekayasa untuk mengelompokkan aset industri ke dalam zona-zona terisolasi.
- Industrial DMZ (IDMZ) bertindak sebagai penyangga netral antara dunia IT korporat dan dunia OT pabrik, mencegah ancaman internet mengeksploitasi PLC secara langsung.
- Perintah kendali fisik (*actuation write command*) wajib dibatasi pada batas Level 1-2, sedangkan data yang diekspos ke Level 4 hanyalah data telemetri historis replikasi bersifat baca-saja (*read-only*).

## Referensi
1. International Society of Automation (ISA), *ANSI/ISA-95.00.01-2010 (IEC 62264-1 Mod) Enterprise-Control System Integration — Part 1: Models and Terminology*, 2010.
2. International Electrotechnical Commission, *IEC 62443-3-3: Security for industrial automation and control systems — System security requirements and security levels*, 2018.
3. National Institute of Standards and Technology (NIST), *Guide to Industrial Control Systems (ICS) Security*, NIST SP 800-82 Rev. 2.

