# Modul B06 — Capstone: Edge Predictive Maintenance System with High-Speed Sampling

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Mengintegrasikan seluruh kompetensi pemantauan kondisi industri (B01–B05) ke dalam satu platform sistem edge end-to-end.
2. Menerapkan pipeline akuisisi getaran frekuensi tinggi (10 kHz) bebas buffer overflow.
3. Mendeteksi dan mendiagnosis inisiasi cacat cincin luar bantalan (BPFO) di bawah derau mesin normal.
4. Memverifikasi seluruh sistem terhadap 4 Skenario Uji Penerimaan Sistem (SATC-B01 hingga SATC-B04) dengan rubrik 100 poin.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 30, Chapter 40.
- Modul Jalur Peminatan Prasyarat: Modul B01, Modul B02, Modul B03, Modul B04, Modul B05.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Spesifikasi Arsitektur Sistem Capstone IIoT
Proyek Capstone Track B mengintegrasikan seluruh rantai instrumentasi industri ke dalam sebuah arsitektur terpadu:
1. **Lapisan Fisik (Level 0)**: Transduser getaran piezoelektrik IEPE dipasang menggunakan dudukan baut stud kaku untuk menjamin bandwidth linier hingga 10 kHz.
2. **Lapisan Edge Computing (Level 1/2)**: Mikrokontroler/Edge PC menjalankan pipeline DMA buffer ganda, menghitung fitur statistik domain waktu, mengeksekusi Transformasi Hilbert untuk spektrum selubung, dan mengklasifikasikan keparahan getaran sesuai standar ISO 20816.
3. **Lapisan Jaringan & Keamanan (Level 3/IDMZ)**: Seluruh metrik getaran dipublikasikan ke server OPC UA terstruktur dan ditransmisikan melintasi Industrial DMZ tanpa melanggar batasan kedaulatan kendali lokal pabrik.

### 2. Landasan Matematis: Metrik Evaluasi Kinerja Sistem Capstone (Mathematical Foundations)

1. **Kecepatan Getaran True RMS (ISO 20816 Velocity Integral)**:
   $$
   v(t) = int a(t) , dt implies V_{	ext{RMS}} = sqrt{rac{1}{N} sum_{i=1}^{N} v_i^2}
   $$

2. **Kriteria Peringatan Dini Cacat Bantalan Komposit**:
   Status alarm anomali diaktifkan jika kondisi kombinasi berikut terpenuhi:
   $$
   	ext{Alarm}_{	ext{Bearing}} = left( 	ext{Kurtosis} > 4{,}5 ight) land left( max_{f in [	ext{BPFO}-delta, 	ext{BPFO}+delta]} S_{	ext{env}}(f) > 3 cdot sigma_{	ext{floor}} ight)
   $$

3. **Verifikasi Ketersediaan & Waktu Tanggap Trip (Worked Example)**:
   Pada kondisi getaran darurat Zona D ($V_{	ext{RMS}} > 4{,}5	ext{ mm/s}$), sistem edge mengeksekusi penghentian darurat motor listrik (*Safe State Trip*). Total waktu henti keselamatan:
   $$
   T_{	ext{trip}} = t_{	ext{sampling}} + t_{	ext{compute}} + t_{	ext{relay}} = 20	ext{ ms} + 15	ext{ ms} + 10	ext{ ms} = 45	ext{ ms}
   $$
   Waktu tanggap $45	ext{ ms}$ berada jauh di bawah batas waktu kerusakan mekanis katastropik motor ($500	ext{ ms}$), membuktikan efektivitas sistem proteksi otonom edge.

## Latihan

### Soal 1: Evaluasi Keparahan ISO 20816 (C3)
Sebuah motor induksi 45 kW pada pompa air beroperasi dengan getaran terukur $V_{	ext{RMS}} = 3{,}6	ext{ mm/s}$. Tentukan Zona Keparahan getaran motor tersebut dan tindakan pemeliharaan yang disyaratkan!

### Soal 2: Verifikasi Logika Interlock Capstone (C4)
Jelaskan alur eksekusi logika pengontrol edge saat Kurtosis bernilai 8.2 namun $V_{	ext{RMS}}$ masih berada di Zona A! Apakah motor harus langsung dimatikan atau dijadwalkan inspeksi bantalan?

## Tugas

## Laporan Rekayasa Lengkap Proyek Capstone Predictive Maintenance

Susun laporan teknik komprehensif implementasi platform Edge PdM:
1. Dokumentasikan arsitektur sistem perangkat lunak dan diagram interaksi komponen.
2. Sajikan hasil eksekusi 4 skenario uji penerimaan sistem (SATC) lengkap dengan grafik bentuk gelombang sinyal.
3. Hitung estimasi penghematan biaya operasional (*Return on Investment* / ROI) dari pencegahan downtime katastropik pabrik.
4. Lampirkan rubrik penilaian mandiri 100 poin.

## Ringkasan
- Modul B06 memberikan pemahaman mendalam dan terapan mengenai Capstone: Edge Predictive Maintenance System with High-Speed Sampling pada tingkat kedalaman L4: Research Preparation.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [industrial_pdm_capstone_platform.py](src/industrial_pdm_capstone_platform.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. ISO 20816-1:2016 Mechanical vibration — Measurement and evaluation of machine vibration, [https://www.iso.org/standard/63124.html](https://www.iso.org/standard/63124.html) (diperiksa 2026-11-18).
2. IEC 62541-1:2020 OPC Unified Architecture - Overview and Concepts, [https://webstore.iec.ch/publication/65040](https://webstore.iec.ch/publication/65040) (diperiksa 2026-11-18).
3. IEC 61508 Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems, [https://www.iec.ch/functional-safety](https://www.iec.ch/functional-safety) (diperiksa 2026-11-18).
