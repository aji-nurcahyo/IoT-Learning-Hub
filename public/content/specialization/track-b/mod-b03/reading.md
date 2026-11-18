# Modul B03 — Industrial Fieldbus Engineering: Modbus RTU/TCP, OPC UA Information Models & TSN

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami karakteristik fisik saluran diferensial RS-485 dan pantulan gelombang transmisi.
2. Menghitung waktu siklus refresh rate polling bus Modbus RTU multi-drop deterministik.
3. Membangun pohon ruang alamat objek dan variabel terstruktur pada server OPC UA.
4. Mengevaluasi batas latensi komunikasi industri deterministik (Time-Sensitive Networking).

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 16, Chapter 33.
- Modul Jalur Peminatan Prasyarat: Modul B01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Karakteristik Saluran RS-485 & Terminasi Saluran
Komunikasi industri Modbus RTU beroperasi di atas lapisan fisik balanced differential line EIA/TIA-485. Sinyal dikirimkan sebagai beda tegangan antara jalur $A$ ($D-$) dan jalur $B$ ($D+$). Untuk mencegah pantulan gelombang elektromagnetik (*transmission line reflections*), kedua ujung fisik bus wajib diterminasi menggunakan resistor terminasi $R_T = 120,Omega$ yang cocok dengan impedansi karakteristik kabel pasangan berpilin (*twisted pair*).

### 2. Model Informasi OPC Unified Architecture (OPC UA)
Berbeda dengan register heksadesimal Modbus yang tidak memiliki semantik konteks, OPC UA (IEC 62541) menyajikan arsitektur berbasis objek (*Object-Oriented Information Model*). Setiap titik data direpresentasikan sebagai **Node** yang memiliki NodeId, BrowseName, Value, DataType, serta relasi (*References*) terstruktur (seperti HasComponent, Organizes, GeneratesEvent).

### 3. Landasan Matematis: Analisis Waktu Siklus Polling Bus & Throughput (Mathematical Foundations)

1. **Waktu Transmisi Frame Serial**:
   Untuk panjang frame $L$ byte pada baud rate $B$ bps (10 bit per karakter):
   $$
   T_{	ext{frame}} = rac{10 cdot L}{B}
   $$

2. **Total Waktu Siklus Polling $N$ Simpul Slave (Worked Example)**:
   Sebuah loop master mem-polling $N = 16$ sensor getaran pada baud rate $B = 19200	ext{ bps}$.
   - Frame Request: $L_{	ext{req}} = 8	ext{ byte} implies T_{	ext{req}} = rac{80}{19200} approx 4{,}17	ext{ ms}$.
   - Waktu turnaround komputasi slave: $t_{	ext{turnaround}} = 5{,}00	ext{ ms}$.
   - Frame Response (10 register float): $L_{	ext{resp}} = 25	ext{ byte} implies T_{	ext{resp}} = rac{250}{19200} approx 13{,}02	ext{ ms}$.
   - Waktu hening inter-frame: $t_{3{,}5} = 3{,}5 	imes rac{10}{19200} approx 1{,}82	ext{ ms}$.
   Total waktu per slave:
   $$
   T_{	ext{slave}} = 4{,}17 + 5{,}00 + 13{,}02 + 1{,}82 = 24{,}01	ext{ ms}
   $$
   Total waktu siklus satu putaran penuh:
   $$
   T_{	ext{cycle}} = 16 	imes 24{,}01	ext{ ms} = 384{,}16	ext{ ms}
   $$
   Laju pembaruan data sistem (*refresh rate*):
   $$
   f_{	ext{refresh}} = rac{1}{T_{	ext{cycle}}} approx 2{,}60	ext{ Hz}
   $$
   Analisis ini membuktikan bahwa bus RS-485 Modbus RTU pada 19200 bps hanya mampu memberikan refresh rate $sim 2{,}6	ext{ Hz}$, sehingga data getaran waveform berkecepatan tinggi tidak boleh ditransmisikan mentah melainkan harus diekstraksi fiturnya terlebih dahulu di level edge.

## Latihan

### Soal 1: Optimasi Baud Rate (C3)
Jika panjang kabel bus RS-485 adalah $400	ext{ meter}$, evaluasi batas baud rate maksimum yang aman dari efek pelemahan kabel! Apakah baud rate 115200 bps layak digunakan?

### Soal 2: Desain Model Objek OPC UA (C4)
Rancang struktur pohon NodeSet OPC UA untuk sebuah pompa hidrolik cerdas yang memuat komponen Motor, Bearing, dan Valve, lengkap dengan tipe data dan variabel status operasional!

## Tugas

## Perancangan Arsitektur Polling Bus & Pemetaan Data Modbus ke Server OPC UA

Rancang arsitektur akuisisi data pabrik yang mengintegrasikan 8 power meter Modbus RTU ke server SCADA OPC UA:
1. Hitung waktu siklus polling pada variasi baud rate 9600, 19200, dan 38400 bps.
2. Buat skrip simulasi pemetaan holding register Modbus ke variabel OPC UA terstruktur.
3. Analisis mekanisme penanganan timeout jika salah satu slave mengalami kegagalan daya.

## Ringkasan
- Modul B03 memberikan pemahaman mendalam dan terapan mengenai Industrial Fieldbus Engineering: Modbus RTU/TCP, OPC UA Information Models & TSN pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [modbus_polling_cycle_sim.py](src/modbus_polling_cycle_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Modbus Organization, Modbus Application Protocol Specification v1.1b3, [https://modbus.org/specs.php](https://modbus.org/specs.php) (diperiksa 2026-11-18).
2. OPC Foundation, OPC Unified Architecture Specification Part 1: Overview and Concepts, [https://opcfoundation.org/developer-tools/specifications-unified-architecture](https://opcfoundation.org/developer-tools/specifications-unified-architecture) (diperiksa 2026-11-18).
