# Chapter 33: Industrial IoT, Modbus & OPC UA

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami arsitektur Industrial IoT (IIoT) serta membedakan karakteristik kritis domain *Operational Technology* (OT) dan *Information Technology* (IT).
2. Menguasai arsitektur protokol **Modbus RTU** (serial RS-485) dan **Modbus TCP** (Ethernet/IP), termasuk struktur frame dan algoritma *CRC-16*.
3. Merancang pemetaan tabel register industri (*Discrete Inputs*, *Coils*, *Input Registers*, dan *Holding Registers*).
4. Memahami paradigma semantik **OPC Unified Architecture (OPC UA)** dan pemodelan data berorientasi objek (*Information Modeling*).
5. Menganalisis peran *Industrial Edge Gateways* dalam menjembatani protokol legasi pabrik dengan sistem analitik awan modern.

## Prasyarat

- Pemahaman komunikasi serial UART, bus RS-485, dan model OSI (Chapter 07 & 11).
- Konsep jaringan TCP/IP, addressing, dan framing data biner (Chapter 12).
- Pemrograman Python dasar (manipulasi byte array dan modul `struct`).

## Konsep dan teori

### 1. Konvergensi OT vs IT dalam Arsitektur IIoT

Sistem otomasi industri secara historis terisolasi dalam piramida otomasi ISA-95:
- **Level 0/1 (Field & Control)**: Sensor, aktuator, drive, dan *Programmable Logic Controller* (PLC) yang menuntut latensi deterministik tinggi (< 10 ms) dan ketersediaan 99.999% (*safety-critical*).
- **Level 2 (Supervisory)**: *Supervisory Control and Data Acquisition* (SCADA) dan *Human-Machine Interface* (HMI) untuk pengawasan operator.
- **Level 3 (Manufacturing Operations)**: *Manufacturing Execution Systems* (MES) untuk penjadwalan produksi.
- **Level 4 (Enterprise)**: *Enterprise Resource Planning* (ERP) dan analitik awan.

```
       +-----------------------------------------------+
       |  Level 4: Enterprise & Cloud Analytics (IT)   |
       +-----------------------------------------------+
                              |  (MQTT / HTTPS / REST)
       +-----------------------------------------------+
       |  Level 3: Operations & MES (IT/OT Bridge)     |
       +-----------------------------------------------+
                              |  (OPC UA / Industrial Ethernet)
       +-----------------------------------------------+
       |  Level 2: SCADA & HMI Monitoring             |
       +-----------------------------------------------+
                              |  (Modbus TCP / PROFINET)
       +-----------------------------------------------+
       |  Level 1: Programmable Logic Controller (PLC) |
       +-----------------------------------------------+
                              |  (Modbus RTU / RS-485)
       +-----------------------------------------------+
       |  Level 0: Physical Sensors & Actuators (OT)   |
       +-----------------------------------------------+
```

Tantangan utama konvergensi OT/IT adalah perbedaan prioritas: OT mengutamakan **Availability & Safety**, sedangkan IT secara historis mengutamakan **Confidentiality & Data Integrity**.

### 2. Protokol Modbus: RTU vs TCP

Modbus (diciptakan oleh Modicon pada 1979) adalah standar komunikasi de facto tertua di lantai pabrik. Model data Modbus terdiri dari 4 tabel memori:

| Tabel Data | Tipe Objek | Akses | Rentang Alamat Standar |
|---|---|---|---|
| **Discretes Input** | Biner (1 bit) | Read-Only | `10001 – 19999` |
| **Coils** | Biner (1 bit) | Read / Write | `00001 – 09999` |
| **Input Registers** | Integer 16-bit | Read-Only | `30001 – 39999` |
| **Holding Registers** | Integer 16-bit | Read / Write | `40001 – 49999` |

#### Struktur Frame Modbus RTU:
```
+--------------+---------------+-------------------+------------------+-----------------+
| Slave ID     | Function Code | Data Offset / Qty | Payload Data     | CRC-16 Checksum |
| (1 Byte)     | (1 Byte)      | (2-4 Bytes)       | (N Bytes)        | (2 Bytes, Little|
+--------------+---------------+-------------------+------------------+-----------------+
```

#### Perhitungan CRC-16:
Frame RTU diproteksi oleh polinomial $0xA001$ dengan nilai inisialisasi $0xFFFF$. Verifikasi integritas bit ini mencegah kesalahan baca akibat interferensi derau elektromagnetik motor industri.

### 3. OPC Unified Architecture (OPC UA)

Modbus memiliki keterbatasan fatal: tidak membawa informasi konteks (metadata) dan tidak memiliki lapisan keamanan bawaan. Register `40001 = 255` tidak menjelaskan apakah itu suhu, tekanan, satuan Celcius atau Fahrenheit.

**OPC UA (IEC 62541)** mengatasi masalah ini melalui:
1. **Semantik & Information Modeling**: Data dimodelkan sebagai grafik berarah (*Node Tree*) yang terdiri dari objek (*Objects*), variabel (*Variables*), tipe data (*DataTypes*), dan relasi antar-node (*References*). Setiap nilai membawa stempel waktu (*Timestamp*) dan indikator mutu data (*Quality Flag*).
2. **Keamanan Bawaan**: Mendukung enkripsi simetris (AES-128/256), penandatanganan digital sertifikat X.509, serta otentikasi berbasis peran pengguna.
3. **Komunikasi Multi-Platform**: Beroperasi di atas port TCP biner murni (`opc.tcp://`) maupun PubSub di atas broker MQTT/UDP.

### 3.1 Landasan Matematis: Polinomial CRC-16 Modbus & Verifikasi Integritas Frame (Mathematical Foundations)

Komunikasi industri (IIoT) mengandalkan Cyclic Redundancy Check (CRC-16) standar Modbus untuk mendeteksi galat transmisi di lingkungan pabrik yang penuh gangguan elektromagnetik:

1. **Polinomial Pembagi CRC-16 (Modbus Standard)**:
   Algoritma CRC-16 Modbus menggunakan representasi polinomial biner:
   $$
   G(x) = x^{16} + x^{15} + x^2 + 1 \quad (\text{heksadesimal: } \texttt{0x8005}, \text{ reversed: } \texttt{0xA001})
   $$
   Register CRC diinisialisasi dengan nilai `0xFFFF`. Setiap byte data di-XOR dengan 8 bit terendah register, kemudian digeser ke kanan sebanyak 8 kali dengan conditional XOR terhadap polinomial `0xA001`.

2. **Kemampuan Deteksi Galat & Analisis Probabilitas Residual Error (Worked Example)**:
   Secara teoritis, CRC-16 menjamin deteksi $100\%$ terhadap seluruh galat bit tunggal (*single-bit error*), galat bit ganda (*double-bit error*), dan pola rentetan galat (*burst error*) dengan panjang $\le 16\text{ bit}$.
   Probabilitas galat acak yang lolos dari deteksi CRC-16 pada frame data sembarang adalah:
   $$
   P_{\text{undetected}} = \frac{1}{2^{16}} = \frac{1}{65536} \approx 1{,}526 \times 10^{-5} \quad (0{,}0015\%)
   $$
   Untuk frame Modbus RTU standar dengan panjang $L = 8\text{ byte}$ pada baud rate $9600\text{ bps}$ ($T_{\text{char}} = 1{,}04\text{ ms}$), waktu transmisi frame total adalah:
   $$
   T_{\text{frame}} = 8 \times 10 \times \frac{1}{9600} \approx 8{,}33\text{ ms}
   $$
   Waktu hening antar-frame minimum (*silent interval*) yang disyaratkan standar Modbus adalah $t_{3{,}5} = 3{,}5 \times T_{\text{char}} \approx 3{,}65\text{ ms}$, memastikan demarkasi frame tanpa memerlukan karakter khusus pembungkus paket.

## Latihan

1. **Analisis Frame Modbus**: Diketahui frame respon Modbus RTU: `01 03 04 00 FF 02 8C CA C6`. Uraikan arti setiap byte:
   - Berapa Slave ID pengirim?
   - Berapa Function Code yang dieksekusi?
   - Berapa jumlah byte data payload yang dikembalikan?
   - Berapa nilai heksadesimal dan desimal dari dua holding register pertama?
2. **Keterbatasan Register 16-bit**: Bagaimana cara membaca nilai bilangan desimal pecahan berpresisi tinggi (*32-bit IEEE 754 Float*) menggunakan register Modbus yang hanya berukuran 16 bit? Jelaskan konsep *Word Swapping* (Big-Endian vs Little-Endian byte ordering).
3. **OPC UA NodeId Structure**: Jelaskan struktur pengidentifikasi node `ns=2;s=Machine1.SpindleSpeed`. Apa arti parameter `ns` (Namespace Index) dan `s` (String Identifier)?

## Tugas

Kembangkan modul simulasi protokol industri Python (`industrial_protocol_sim.py`) yang memverifikasi pembacaan frame Modbus RTU Function Code 03 lengkap dengan perhitungan CRC-16 biner, serta navigasi hierarki *Information Model* OPC UA. Ujilah parsing data telemetri sensor analog dan verifikasi kesesuaian nilai register dengan pembacaan terstruktur.

## Ringkasan

1. Industri modern bertransisi dari piramida otomasi kaku (ISA-95) menuju arsitektur IIoT terkonvergensi yang fleksibel.
2. Modbus RTU/TCP menyediakan komunikasi register berkecepatan tinggi yang sederhana namun rentan dan tanpa metadata semantik.
3. OPC UA menjadi standar interoperabilitas global berkat pemodelan data berorientasi objek yang kaya konteks dan enkripsi sertifikat kriptografi tingkat militer.

## Referensi
- Modbus Organization, *Modbus Application Protocol Specification V1.1b3*, Modbus.org, 2012.
- IEC 62541-1:2020, *OPC Unified Architecture - Part 1: Overview and Concepts*, International Electrotechnical Commission.

1. Modbus Organization. *Modbus Application Protocol Specification V1.1b3*. 2012.
2. OPC Foundation. *OPC Unified Architecture Specification Part 1-5 (IEC 62541)*. 2023.
3. Boyes, H., et al. *The Industrial Internet of Things (IIoT): An Analysis Framework*. Computers in Industry, Vol. 101, 2018.
