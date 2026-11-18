# Modul B02 — High-Frequency Vibration, Acoustic Emission & Sensor Installation Physics

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami prinsip kerja transduser piezoelektrik IEPE dan respons frekuensi alami massa-pegas sensor getaran.
2. Menghitung frekuensi resonansi kontak mekanis berdasarkan kekakuan dudukan (stud, magnet, lilin perekat).
3. Menganalisis fenomena emisi akustik ultrasonik (20 kHz–100 kHz) untuk deteksi keretakan mikro dini.
4. Merancang filter anti-aliasing analog/digital dan menentukan batas frekuensi linier pengukuran (ISO 20816).

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 07, Chapter 08, Chapter 35.
- Modul Jalur Peminatan Prasyarat: Modul B01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Karakteristik Transduser Piezoelektrik IEPE/ICP
Transduser getaran industri standar menggunakan elemen kristal piezoelektrik (seperti kuarsa atau PZT) yang menghasilkan muatan listrik proporsional terhadap gaya akselerasi mekanis. Rangkaian internal IEPE (*Integrated Electronics Piezo-Electric*) mengonversi muatan berimpedansi sangat tinggi menjadi sinyal tegangan berimpedansi rendah yang dapat ditransmisikan melalui kabel koaksial hingga ratusan meter.

### 2. Fisika Resonansi Pemasangan (Sensor Mounting Resonance)
Sensor akselerometer yang dipasang pada permukaan mesin membentuk sistem osilator mekanis harmonik teredam orde-dua (massa sensor $m$ dan konstanta pegas kontak dudukan $k$). Pada frekuensi eksitasi mendekati frekuensi resonansi alami ($f_n$), sinyal getaran mengalami amplifikasi resonansi ekstrem yang merusak akurasi pengukuran. Standar rekayasa menetapkan batas frekuensi pengukuran yang valid hanyalah pada rentang $f le 0{,}2 cdot f_n$.

### 3. Landasan Matematis: Resonansi Kontak & Syarat Nyquist Anti-Aliasing (Mathematical Foundations)

1. **Frekuensi Resonansi Kontak Alami**:
   $$
   f_n = rac{1}{2pi} sqrt{rac{k_{	ext{mount}}}{m_{	ext{sensor}}}}
   $$
   Batas linier pengukuran ($pm 5%$ toleransi amplitudo):
   $$
   f_{	ext{usable}} le 0{,}20 cdot f_n
   $$

2. **Perhitungan Filter Anti-Aliasing (Worked Example)**:
   Sebuah sistem mengakuisisi sinyal emisi akustik ultrasonik hingga frekuensi maksimum $f_{	ext{max}} = 25	ext{ kHz}$.
   Menurut Teorema Sampling Nyquist-Shannon, frekuensi sampling minimum adalah:
   $$
   f_s > 2 cdot f_{	ext{max}} = 50	ext{ kHz}
   $$
   Jika digunakan filter analog Butterworth orde-4 dengan redaman $-24	ext{ dB/oktaf}$ pada frekuensi cut-off $f_c = 25	ext{ kHz}$, untuk meredam komponen desah aliasing sebesar $48	ext{ dB}$ pada frekuensi sampling, maka $f_s$ dipilih pada dua oktaf di atas $f_c$:
   $$
   f_s = 4 cdot f_c = 100	ext{ kHz}
   $$

## Latihan

### Soal 1: Pengaruh Massa Sensor (C3)
Sebuah akselerometer miniatur bermassa $m = 5	ext{ gram}$ dan akselerometer industri standar bermassa $m = 50	ext{ gram}$ dipasang pada dudukan magnet yang sama ($k = 1{,}2 	imes 10^7	ext{ N/m}$). Hitung frekuensi resonansi kedua sensor dan bandingkan batas bandwidth pengukuran masing-masing!

### Soal 2: Desain Filter Anti-Aliasing (C4)
Anda diminta merancang sistem pemantauan getaran gearbox dengan frekuensi meshing gear maksimum $f_{	ext{mesh}} = 4{,}8	ext{ kHz}$. Tentukan frekuensi cut-off filter low-pass dan laju sampling ADC yang disarankan agar terhindar dari distorsi aliasing!

## Tugas

## Analisis Pemilihan Sensor Getaran & Metode Mounting Motor Induksi 3000 RPM

Rancang dokumen spesifikasi instrumentasi getaran untuk motor induksi 3000 RPM yang menggerakkan kompresor gas berkecepatan tinggi:
1. Hitung frekuensi putar poros dasar ($f_r$) dan perkiraan harmonik ke-10.
2. Bandingkan 3 metode mounting (baut stud, magnetik, lilin perekat) terhadap spektrum yang ingin diamati.
3. Buat skrip Python simulasi respons frekuensi filter anti-aliasing.

## Ringkasan
- Modul B02 memberikan pemahaman mendalam dan terapan mengenai High-Frequency Vibration, Acoustic Emission & Sensor Installation Physics pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [vibration_mounting_sim.py](src/vibration_mounting_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. ISO 20816-1:2016 Mechanical vibration — Measurement and evaluation of machine vibration, [https://www.iso.org/standard/63124.html](https://www.iso.org/standard/63124.html) (diperiksa 2026-11-18).
2. PCB Piezotronics, Introduction to Piezoelectric Accelerometers and Mounting Techniques, [https://www.pcb.com/sensors-for-test-measurement/accelerometers](https://www.pcb.com/sensors-for-test-measurement/accelerometers) (diperiksa 2026-11-18).
