# Modul D02 — Edge Feature Engineering, Signal Preprocessing & Dimensionality Reduction

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Merancang filter digital IIR Biquad bertingkat menggunakan aritmatika integer fixed-point.
2. Mengimplementasikan bank filter skala Mel dan ekstraksi koefisien MFCC berdaya komputasi rendah.
3. Menerapkan reduksi dimensi Principal Component Analysis (PCA) untuk pemadatan ruang fitur sensor.
4. Membangun pipeline pra-pemrosesan sinyal streaming bebas alokasi heap dinamis.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 05, Chapter 23, Chapter 35.
- Modul Jalur Peminatan Prasyarat: Modul D01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Ekstraksi Fitur Akustik Mel-Frequency Cepstral Coefficients (MFCC)
Dalam pemantauan akustik mesin dan pengenalan audio edge, transmisi data waveform mentah berkecepatan 16 kHz membutuhkan bandwidth dan memori yang sangat besar. **MFCC** mereduksi dimensi data audio dengan memetakan spektrum daya ke dalam skala frekuensi non-linear Mel yang menyerupai persepsi koklea telinga manusia, kemudian menerapkan Transformasi Kosinus Diskrit (DCT) untuk mendekorelasikan energi bank filter menjadi vektor koefisien kompak (10–13 koefisien per frame).

### 2. Aritmatika Fixed-Point Q-Format pada Mikrokontroler
Pada prosesor mikrokontroler berdaya ultra-rendah tanpa FPU perangkat keras, operasi floating-point disimulasikan melalui perangkat lunak yang lambat. Format **Q15** menggunakan bilangan bulat bertanda 16-bit (*int16_t*) di mana 1 bit menyatakan tanda dan 15 bit menyatakan fraksi desimal:
$$
	ext{Nilai Riil} = rac{N_{	ext{integer}}}{2^{15}} = rac{N_{	ext{integer}}}{32768}
$$
Operasi perkalian fixed-point dieksekusi dengan satu instruksi perkalian 32-bit hardware diikuti pergeseran bit (*bit-shift*) arithmetic right shift (shift-kanan 15), menghasilkan kecepatan komputasi puluhan kali lebih cepat dibanding float32.

### 3. Landasan Matematis: Konversi Skala Mel & Persamaan Biquad Filter IIR (Mathematical Foundations)

1. **Konversi Frekuensi Linier $f$ (Hz) ke Skala Mel $m$**:
   $$
   m = 2595 log_{10} left( 1 + rac{f}{700} ight)
   $$

2. **Transformasi Kosinus Diskrit (DCT-II) untuk Koefisien MFCC ke-$k$**:
   $$
   c_k = sum_{m=0}^{M-1} log(S_m) cdot cosleft( rac{pi k (m + 0{,}5)}{M} ight)
   $$
   di mana $S_m$ adalah energi bank filter Mel ke-$m$, dan $M$ adalah total filterbank.

**Worked Numerical Example**:
Konversi frekuensi nada ultrasonik $f = 3500	ext{ Hz}$ ke skala Mel:
$$
m = 2595 log_{10} left( 1 + rac{3500}{700} ight) = 2595 log_{10}(1 + 5) = 2595 log_{10}(6)
$$
Karena $log_{10}(6) approx 0{,}77815$:
$$
m = 2595 	imes 0{,}77815 approx 2019{,}3	ext{ Mel}
$$
Pemetaan non-linear ini memadatkan spektrum frekuensi tinggi dan memberikan resolusi lebih tajam pada frekuensi menengah bawah tempat getaran mekanis dominan berada.

## Latihan

### Soal 1: Konversi Format Q15 (C3)
Konversikan bilangan desimal $x = 0{,}625$ dan $y = -0{,}25$ ke dalam representasi heksadesimal integer 16-bit format Q15!

### Soal 2: Evaluasi Reduksi Dimensi PCA (C4)
Sebuah sistem pemantauan getaran mengukur 16 fitur domain waktu dan frekuensi. Analisis PCA menunjukkan bahwa 3 komponen utama pertama memiliki rasio varians kumulatif sebesar $94{,}8%$. Berikan rekomendasi teknis mengenai jumlah fitur yang harus dipertahankan untuk menghemat memori TinyML!

## Tugas

## Perancangan Pipeline Ekstraksi Fitur Akustik Fixed-Point pada Mikrokontroler

Rancang modul ekstraksi fitur streaming sinyal sensor:
1. Implementasikan filter digital IIR Biquad lolos-tinggi untuk menghilangkan desah offset DC.
2. Buat fungsi ekstraksi koefisien MFCC berbasis aritmatika integer fixed-point Q15.
3. Uji pipeline pada dataset rekaman suara bantalan normal dan bantalan aus, serta sajikan perbandingan akurasi representasi terhadap komputasi float32.

## Ringkasan
- Modul D02 memberikan pemahaman mendalam dan terapan mengenai Edge Feature Engineering, Signal Preprocessing & Dimensionality Reduction pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [fixed_point_mfcc_extractor_sim.py](src/fixed_point_mfcc_extractor_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Oppenheim, A. V., & Schafer, R. W., Discrete-Time Signal Processing, Pearson, [https://www.pearson.com/en-us/subject-catalog/p/discrete-time-signal-processing/P200000003254](https://www.pearson.com/en-us/subject-catalog/p/discrete-time-signal-processing/P200000003254) (diperiksa 2026-11-18).
2. Davis, S., & Mermelstein, P., Comparison of Parametric Representations for Monosyllabic Word Recognition, IEEE ASSP, 1980, [https://ieeexplore.ieee.org/document/1163420](https://ieeexplore.ieee.org/document/1163420) (diperiksa 2026-11-18).
