# Chapter 35: Edge AI, TinyML & Sensor Inference

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami perbedaan fundamental antara arsitektur *Cloud AI* tersentralisasi dan *Edge AI / TinyML* terdistribusi.
2. Menguasai alur kerja TinyML lengkap: akuisisi sinyal sensor, reduksi dimensi melalui ekstraksi fitur statistik, pelatihan model, kuantisasi, dan *deployment*.
3. Mengimplementasikan algoritma ekstraksi fitur domain waktu (*Mean, Root Mean Square, Peak-to-Peak, Zero Crossing Rate*).
4. Menganalisis teknik kuantisasi bilangan bulat **INT8** (*Post-Training Quantization*) dan dampaknya terhadap reduksi memori SRAM/Flash serta komputasi fixed-point.
5. Mengevaluasi batasan keras mikrokontroler (*memory footprint*, latensi inferensi, konsumsi energi) dan akurasi model pada deteksi anomali getaran mesin.

## Prasyarat

- Pemahaman pengolahan sinyal digital dasar dan sampling data (Chapter 05).
- Konsep dasar aljabar linear (perkalian matriks dan dot product) serta statistik deskriptif.
- Pemrograman Python dasar (list comprehension dan operasi matematika).

## Konsep dan teori

### 1. Paradigma Cloud AI vs Edge AI (TinyML)

Mengirimkan seluruh aliran data sensor mentah berfrekuensi tinggi (misalnya akselerometer 1 kHz atau sinyal audio 16 kHz) ke cloud memiliki kelemahan fatal:
- **Bandwidth & Biaya**: Mengunggah ribuan megabyte data per hari menguras kuota seluler dan membebani jaringan.
- **Latensi**: *Round-trip time* internet (50–500 ms) terlalu lambat untuk sistem keselamatan pengereman darurat atau pemutus sirkuit.
- **Privasi**: Data sensitif (suara, gerak tubuh, telemetri medis) rentan disadap saat transit melintasi internet publik.
- **Ketersediaan**: Sistem menjadi tidak berguna saat koneksi nirkabel padam.

**TinyML** membawa model inferensi kecerdasan buatan langsung ke dalam mikrokontroler hemat energi (seperti ARM Cortex-M atau ESP32) dengan konsumsi daya di bawah 1 miliwatt.

```
+-------------------------------------------------------------+
|                 Alur Kerja Rekayasa TinyML                  |
+-------------------------------------------------------------+
   [1. Sensor Sampling] -> Akselerometer / IMU (Frekuensi 100 Hz - 1 kHz)
          |
          v
   [2. Feature Extraction] -> Reduksi Dimensi: RMS, P2P, Mean, ZCR
          |
          v
   [3. Model Training] -> Neural Network / Dense Layer (FP32)
          |
          v
   [4. Quantization] -> Konversi FP32 ke INT8 (Skala 4x Lebih Padat)
          |
          v
   [5. Embedded Deployment] -> Eksekusi Fixed-Point pada SRAM Mikrokontroler
```

### 2. Ekstraksi Fitur Domain Waktu

Sinyal getaran dari mesin industri (*predictive maintenance*) dikumpulkan dalam jendela waktu geser (*sliding window* $N$ sampel):

1. **Mean ($\mu$)**: Titik tengah pergeseran sinyal:
   $$\mu = \frac{1}{N} \sum_{i=1}^{N} x_i$$
2. **Root Mean Square (RMS)**: Indikator utama energi total dan intensitas getaran mekanis:
   $$\text{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} x_i^2}$$
3. **Peak-to-Peak (P2P)**: Rentang simpangan ekstrem gelombang ($x_{max} - x_{min}$).
4. **Zero Crossing Rate (ZCR)**: Frekuensi sinyal melintasi sumbu nol, mencerminkan komponen frekuensi dominan tanpa perlu menghitung Fast Fourier Transform (FFT) yang boros CPU.

### 3. Kuantisasi Bilangan Bulat INT8 (Quantization)

Model deep learning standar menggunakan bilangan pecahan 32-bit *Floating-Point* (`float32`). Pada mikrokontroler tanpa *Floating Point Unit* (FPU) perangkat keras, operasi floating-point disimulasikan melalui perangkat lunak yang memakan banyak siklus instruksi.

**Kuantisasi INT8** memetakan nilai float kontinu $[a, b]$ ke dalam rentang integer 8-bit bertanda $[-128, 127]$:

$$q = \text{round}\left(\frac{x}{S}\right) + Z$$

Di mana:
- $S$ (*Scale factor*): rasio penskalaan presisi bilangan pecahan per langkah integer.
- $Z$ (*Zero point*): pergeseran nilai nol riil dalam domain terkuantisasi.

### 4. Landasan Matematis: Propagasi Kuantisasi Matriks Bobot & Worked Numerical Example (Mathematical Foundations)

Operasi inferensi jaringan saraf tiruan (Dense layer) dengan $M$ input fitur $x \in \mathbb{R}^M$ dan matriks bobot $W \in \mathbb{R}^{K \times M}$ menghasilkan vektor aktivasi $y \in \mathbb{R}^K$:
$$
y_k = \sum_{j=1}^{M} W_{kj} x_j + b_k
$$
Saat bobot $W$ dan aktivasi $x$ dikuantisasi menjadi INT8 dengan faktor skala masing-masing $S_W, S_x$ dan zero-point $Z_W, Z_x$:
$$
W_{kj} \approx S_W (q_{W,kj} - Z_W), \qquad x_j \approx S_x (q_{x,j} - Z_x)
$$
Substitusi ke perkalian dot product:
$$
y_k \approx S_W S_x \sum_{j=1}^{M} (q_{W,kj} - Z_W)(q_{x,j} - Z_x) + b_k
$$
Jika aktivasi output $y_k$ dikuantisasi kembali ke representasi INT8 $q_{y,k}$ dengan skala $S_y$ dan zero-point $Z_y$:
$$
q_{y,k} = \text{round}\left( \frac{S_W S_x}{S_y} \sum_{j=1}^{M} (q_{W,kj} - Z_W)(q_{x,j} - Z_x) \right) + Z_y
$$
Konstanta pengali pecahan $M_0 = \frac{S_W S_x}{S_y}$ direpresentasikan sebagai perkalian integer fixed-point $M_0 \approx 2^{-n} M_{\text{int}}$ menggunakan operasi bit-shift arithmetic right shift (`>> n`) tanpa memerlukan operasi FPU pembagi perangkat lunak.

**Worked Numerical Example (Kuantisasi dan Inferensi INT8)**:
Diberikan 4 fitur getaran terukur: $\text{Mean} = 0{,}02\text{ g}$, $\text{RMS} = 1{,}80\text{ g}$, $\text{P2P} = 6{,}50\text{ g}$, $\text{ZCR} = 14\text{ crossing}$.
Skala kuantisasi fitur input adalah $S_x = 0{,}05$ dengan $Z_x = 0$.
1. Kuantisasi fitur input menjadi vektor integer INT8:
   $$
   q_{x,1} = \text{round}\left(\frac{0{,}02}{0{,}05}\right) = 0
   $$
   $$
   q_{x,2} = \text{round}\left(\frac{1{,}80}{0{,}05}\right) = 36
   $$
   $$
   q_{x,3} = \text{round}\left(\frac{6{,}50}{0{,}05}\right) = 130 \to \text{saturate}(127) = 127
   $$
   $$
   q_{x,4} = \text{round}\left(\frac{14}{0{,}05}\right) = 280 \to \text{saturate}(127) = 127
   $$
2. Bobot klasifikasi kelas *Bearing Fault* ($k=1$) adalah $q_W = [-10, 45, 80, 20]$ dengan $S_W = 0{,}01$, $Z_W = 0$, dan bias $b_1 = 0$.
3. Akumulasi perkalian integer (menggunakan register akumulator INT32 untuk mencegah overflow):
   $$
   \text{Acc} = \sum_{j=1}^{4} q_{W,j} q_{x,j} = (-10 \times 0) + (45 \times 36) + (80 \times 127) + (20 \times 127)
   $$
   $$
   \text{Acc} = 0 + 1620 + 10160 + 2540 = 14.320
   $$
4. Dequantization skor probabilitas unnormalized:
   $$
   y_1 = S_W \cdot S_x \cdot \text{Acc} = (0{,}01) \times (0{,}05) \times 14320 = 0{,}0005 \times 14320 = 7{,}16
   $$
Skor tinggi $y_1 = 7{,}16$ mengonfirmasi anomali bantalan mekanis secara langsung dari komputasi perkalian integer 8-bit berkecepatan mikrodetik pada mikrokontroler.

### 5. Strategi Deployment & Optimasi CMSIS-NN

Implementasi model TinyML pada prosesor mikrokontroler memanfaatkan pustaka instruksi akselerasi perangkat keras:
- **Pustaka CMSIS-NN / ESP-NN**: Memanfaatkan instruksi SIMD (*Single Instruction, Multiple Data*) yang mampu mengeksekusi empat operasi perkalian akumulasi 8-bit ($4 \times \text{MAC}$) dalam satu siklus clock CPU.
- **Arena Memori Bersama (Tensor Arena)**: Menghindari fragmentasi heap runtime dengan mengalokasikan satu blok array statis byte buffer yang dipakai bergantian oleh setiap layer jaringan secara sekuensial.
- **Deteksi Anomali Tanpa Pengawasan (Autoencoder)**: Untuk sistem dengan sampel kerusakan langka, arsitektur autoencoder dilatih hanya pada getaran normal; lonjakan galat rekonstruksi kuadratik $E_{\text{recon}} = \|x - \hat{x}\|^2 > \theta_{\text{th}}$ menandai timbulnya anomali mekanis baru secara akurat.

## Latihan

1. **Analisis Kuantisasi Input**: Diketahui parameter kuantisasi fitur RMS adalah $S = 0.05$ dan $Z = 0$. Jika nilai pembacaan getaran aktual adalah $\text{RMS} = 1.9035\text{ g}$, hitung nilai integer terkuantisasi $q$ dalam format INT8.
2. **Dampak Sampling Rate**: Mengapa pada aplikasi deteksi anomali akustik ultrasonik (misalnya kebocoran gas bertekanan pada frekuensi 40 kHz), proses ekstraksi fitur lebih disukai dieksekusi di edge daripada mengirimkan sinyal raw audio ke cloud?
3. **Penyusutan Bobot Memori**: Jika sebuah model klasifikasi citra memiliki 150.000 parameter bobot dalam format FP32, berapa kilobyte memori flash yang dihemat jika model tersebut berhasil dikuantisasi penuh ke INT8?

## Tugas

Kembangkan modul simulasi ekstraksi fitur dan klasifikasi TinyML Python (`tinyml_inference_sim.py`) yang:
1. Mengekstraksi empat fitur domain waktu (Mean, RMS, P2P, ZCR) dari jendela data getaran sensor akselerometer.
2. Melakukan inferensi feedforward menggunakan bobot terkuantisasi INT8 untuk membedakan kondisi motor normal versus anomali kerusakan bantalan (*bearing fault*).
3. Membuktikan bahwa skor kelas normal mendominasi pada getaran rendah dan kelas anomali mendominasi saat lonjakan impak mekanis terdeteksi.

## Ringkasan

1. TinyML memungkinkan pemrosesan AI lokal pada mikrokontroler berdaya ultra-rendah dengan latensi instan dan privasi data terjamin.
2. Ekstraksi fitur domain waktu mereduksi aliran data mentah berdimensi tinggi menjadi vektor input padat yang efisien.
3. Kuantisasi INT8 memangkas kebutuhan memori hingga seperempat ukuran semula dan mengakselerasi komputasi aritmatika pada prosesor embedded.

## Referensi

1. Warden, P., & Situnayake, D. *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*. O'Reilly Media, 2020.
2. Ray, P. P. *A Review on TinyML: State-of-the-Art and Prospects*. Journal of King Saud University - Computer and Information Sciences, 2022.
3. ARM Ltd. *CMSIS-NN: Efficient Neural Network Kernels for Arm Cortex-M Processors*. 2023.
