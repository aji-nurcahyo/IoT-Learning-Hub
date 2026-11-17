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

Keunggulan Kuantisasi INT8:
- Ukuran model menyusut sebesar $75\%$ (dari 4 byte menjadi 1 byte per bobot).
- Operasi dot-product dapat memanfaatkan instruksi SIMD integer yang sangat cepat pada core prosesor modern.

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
