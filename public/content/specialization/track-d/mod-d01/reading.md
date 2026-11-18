# Modul D01 — Embedded AI Architecture, Hardware Accelerators & Neural Processing Units

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Membedakan pemrosesan tensor pada arsitektur CPU murni, DSP SIMD, dan Neural Processing Unit (NPU) embedded.
2. Menganalisis batasan memori dan batas throughput komputasi menggunakan Roofline Performance Model.
3. Menghitung intensitas aritmatika (Operational Intensity) dari layer neural network (Dense vs Conv1D).
4. Membangun modul Python estimasi latensi eksekusi berdasarkan model performa perangkat keras.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 04, Chapter 05.
- Modul Jalur Peminatan Prasyarat: Tidak ada (modul awal jalur peminatan).
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Evolusi Pemrosesan Kecerdasan Buatan di Mikrokontroler
Implementasi model jaringan saraf tiruan pada perangkat tertanam (*Embedded AI*) bertransisi melalui tiga generasi arsitektur:
1. **CPU Emulation (Software Floating-Point)**: Seluruh operasi perkalian akumulasi dieksekusi instruksi CPU standar. Lambat dan memboroskan baterai.
2. **DSP Extensions & SIMD (Single Instruction Multiple Data)**: Arsitektur modern (seperti ARM Cortex-M Helium atau Xtensa LX7 ESP32-S3) memuat instruksi vektor yang mampu mengeksekusi 4 atau 8 operasi perkalian INT8 dalam satu siklus clock CPU.
3. **Dedicated Micro-NPU (Neural Processing Unit)**: Coprocessor perangkat keras terdedikasi (misal ARM Ethos-U55) yang mengeksekusi systolic array perkalian matriks secara mandiri tanpa membebani CPU utama.

### 2. Roofline Performance Model
Model Roofline memetakan kinerja komputasi yang dapat dicapai (*Attainable Performance*) sebagai fungsi dari **Intensitas Operasional** ($I$, rasio total operasi komputasi per byte data yang ditransfer dari memori). Garis atap (*Roof*) sistem dibatasi oleh dua batas fisik: batas kecepatan puncak prosesor (*Compute Bound*) dan batas kecepatan bandwidth transfer memori (*Memory Bound*).

### 3. Landasan Matematis: Formulasi Model Roofline & Intensitas Operasional (Mathematical Foundations)

1. **Intensitas Operasional ($I$)**:
   $$
   I = rac{	ext{Total Operasi Komputasi (FLOPs / MACs)}}{	ext{Total Transfer Memori (Bytes)}}
   $$

2. **Kinerja Maksimum Teraih ($P$)**:
   $$
   P = min left( P_{	ext{peak}}, quad I cdot B_{	ext{mem}} ight)
   $$

**Worked Numerical Example**:
Layer konvolusi 1D mengeksekusi $90.000	ext{ operasi MAC}$ dan membutuhkan transfer bobot serta aktivasi sebesar $20.000	ext{ byte}$.
$$
I = rac{90.000	ext{ MAC}}{20.000	ext{ Byte}} = 4{,}5	ext{ MAC/Byte}
$$
Jika dijalankan dari memori SPI Flash dengan bandwidth $B_{	ext{mem}} = 80	ext{ MB/s} = 0{,}08	ext{ GB/s}$:
$$
P_{	ext{mem}} = 4{,}5 	imes 0{,}08 = 0{,}36	ext{ GMAC/s}
$$
Karena batas puncak prosesor adalah $P_{	ext{peak}} = 0{,}80	ext{ GMAC/s}$, eksekusi dari Flash mengalami degradasi $55%$ akibat *memory bottleneck*. Saat bobot model disalin ke memori SRAM internal ($B_{	ext{mem}} = 1{,}6	ext{ GB/s}$):
$$
P_{	ext{sram}} = min(0{,}80, quad 4{,}5 	imes 1{,}6) = min(0{,}80, 7{,}20) = 0{,}80	ext{ GMAC/s}
$$
Sistem mencapai **100% efisiensi komputasi puncak**, membuktikan krusialnya penempatan bobot layer kritis di SRAM/TCM.

## Latihan

### Soal 1: Analisis Intensitas Aritmatika Layer Dense (C3)
Sebuah layer Dense menerima 64 fitur input dan menghasilkan 10 kelas keluaran. Hitung total operasi perkalian-akumulasi (MAC) dan total transfer memori jika bobot berukuran 1 byte (INT8)! Hitung intensitas operasionalnya!

### Soal 2: Evaluasi Roofline NPU (C4)
Sebuah prosesor mikro-NPU memiliki kinerja puncak 2.0 GMAC/s pada 500 MHz dengan bandwidth bus 1.0 GB/s. Berapakah intensitas operasional minimum yang dibutuhkan agar NPU tersebut bekerja pada kapasitas penuhnya?

## Tugas

## Pemodelan Kinerja Hardware Roofline untuk Arsitektur Edge AI TinyML

Rancang studi komparasi analitis kinerja inferensi mikrokontroler target:
1. Buat model Roofline untuk keluarga prosesor ARM Cortex-M4 (tanpa SIMD) vs Cortex-M55 (dengan Helium SIMD).
2. Evaluasi estimasi latensi inferensi model CNN 1D audio klasifikasi pada kedua prosesor.
3. Lampirkan skrip Python perhitungan batas bandwidth memori dan grafik kurva Roofline.

## Ringkasan
- Modul D01 memberikan pemahaman mendalam dan terapan mengenai Embedded AI Architecture, Hardware Accelerators & Neural Processing Units pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [hardware_roofline_model_sim.py](src/hardware_roofline_model_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Williams, S., et al., Roofline: An Insightful Visual Performance Model for Multicore Architectures, Communications of the ACM, 2009, [https://dl.acm.org/doi/10.1145/1498765.1498785](https://dl.acm.org/doi/10.1145/1498765.1498785) (diperiksa 2026-11-18).
2. Arm Ltd, Arm Helium Technology Reference Manual, [https://developer.arm.com/architectures/cpu-architecture/m-profile/helium-technology](https://developer.arm.com/architectures/cpu-architecture/m-profile/helium-technology) (diperiksa 2026-11-18).
