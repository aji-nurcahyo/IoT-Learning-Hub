# Modul D06 — Real-Time Multimodal Edge Vision & Acoustic Anomaly Detection System (Capstone Project)

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. SATC-D01: Mengoperasikan dual-modal processing pipeline (Audio MFCC Q15 + Vision Spatial Gradient).
2. SATC-D02: Membuktikan latensi eksekusi total end-to-end berada di bawah 50 milidetik.
3. SATC-D03: Menerapkan On-Device Late Bayesian Fusion untuk evaluasi tingkat anomali secara lokal.
4. SATC-D04: Memverifikasi batas penggunaan memori (SRAM < 192 KB, Flash < 384 KB) dan profil daya.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 31, Chapter 32, Chapter 33, Chapter 34, Chapter 35, Chapter 36, Chapter 37, Chapter 38, Chapter 39, Chapter 40.
- Modul Jalur Peminatan Prasyarat: Modul D01, Modul D02, Modul D03, Modul D04, Modul D05.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Visi Arsitektur Capstone Track D: Sistem Multimodal Edge AI
Dalam sistem manufaktur modern, deteksi dini kerusakan mekanikal seperti keausan bantalan, kavitasi pompa, atau pergeseran poros memerlukan konvergensi sensor multi-domain. Mengandalkan hanya penglihatan komputer (*computer vision*) rentan terhadap kegelapan, debu industri, dan oklusi mekanis. Sebaliknya, mengandalkan hanya audio akustik rentan terhadap kebisingan latar (*ambient noise*) pabrik.

Capstone Track D mengintegrasikan pemrosesan sinyal akustik berkecepatan tinggi dengan analisis citra spasial terkompresi ke dalam satu edge processor mikrokontroler (misalnya ESP32-S3 atau ARM Cortex-M55/Ethos-U55).

### 2. Kriteria Penerimaan Sistem (Specialization Acceptance Test Criteria - SATC)
Proyek capstone ini diikat oleh 4 kriteria teknis yang ketat:
1. **SATC-D01 (Dual-Modal Processing Pipeline)**: Mengoperasikan dua jalur pemrosesan independen: ekstraksi fitur spektral audio (MFCC format fixed-point Q15) dan spatial gradient histogram citra grayscale berukuran ringkas ($64 \times 64$ atau macro-block gradient).
2. **SATC-D02 (Real-Time End-to-End Latency < 50 ms)**: Seluruh rantai komputasi—mulai dari akuisisi sampel, DSP, eksekusi neural network INT8, hingga fusi log-odds—harus selesai dalam waktu di bawah 50 milidetik.
3. **SATC-D03 (On-Device Bayesian Fusion & Decision Engine)**: Keputusan akhir anomali dihitung secara lokal di perangkat menggunakan formulasi log-odds tanpa dependensi jaringan eksternal.
4. **SATC-D04 (Strict Memory & Energy Budget Verification)**: Alokasi memori tidak boleh melebihi 192 KB SRAM dan 384 KB Flash untuk menjamin headroom operasional RTOS.

### 3. Landasan Matematis: Late Bayesian Fusion dengan Log-Likelihood Ratio (LLR)

1. **Teorema Bayes pada Multiple Evidence Independen**:
   $$
   P(\text{Fault} \mid \mathbf{z}_A, \mathbf{z}_V) = \frac{P(\mathbf{z}_A, \mathbf{z}_V \mid \text{Fault}) P(\text{Fault})}{P(\mathbf{z}_A, \mathbf{z}_V)}
   $$

2. **Transformasi ke Ruang Log-Odds**:
   $$
   \text{Odds}(\text{Fault} \mid \mathbf{z}_A, \mathbf{z}_V) = \frac{P(\text{Fault} \mid \mathbf{z}_A, \mathbf{z}_V)}{P(\neg \text{Fault} \mid \mathbf{z}_A, \mathbf{z}_V)}
   $$
   $$
   \ln \text{Odds} = \ln \text{Odds}_0 + \ln \frac{P(\mathbf{z}_A \mid \text{Fault})}{P(\mathbf{z}_A \mid \neg \text{Fault})} + \ln \frac{P(\mathbf{z}_V \mid \text{Fault})}{P(\mathbf{z}_V \mid \neg \text{Fault})}
   $$
   $$
   L_{\text{post}} = L_0 + \text{LLR}_A + \text{LLR}_V
   $$

3. **Rekonstruksi Probabilitas Anomali Terfusi**:
   $$
   P(\text{Fault} \mid \mathbf{z}_A, \mathbf{z}_V) = \sigma(L_{\text{post}}) = \frac{1}{1 + e^{-L_{\text{post}}}}
   $$
   di mana $\sigma(\cdot)$ adalah fungsi sigmoid logistik standar.

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa sistem multimodal capstone menggunakan Late Bayesian Fusion dibanding Early Fusion (menggabungkan sinyal audio mentah dan piksel kamera sebelum model)?**
   - *Jawaban*: Late Fusion memisahkan pipeline ekstraksi domain-spesifik berkecepatan berbeda, mereduksi kebutuhan sinkronisasi memori data mentah yang besar di SRAM, dan meningkatkan ketahanan sistem jika salah satu sensor mengalami gangguan.

2. **Sesuai kriteria penerimaan SATC-D02, batas latensi maksimum end-to-end dari pengambilan sampel sensor hingga evaluasi alarm adalah:**
   - *Jawaban*: 50 milidetik, guna menjamin respons proteksi mesin sebelum kerusakan mekanis katastropik terjadi.

## Tugas

## Penugasan Mandiri

Rancang arsitektur sistem deteksi anomali multimodal audio-vision pada mikrokontroler target. Tunjukkan bukti bahwa pemakaian memori statis SRAM berada di bawah 192 KB dan total waktu inferensi end-to-end di bawah 50 milidetik.

## Ringkasan
- Modul D06 memberikan pemahaman mendalam dan terapan mengenai Real-Time Multimodal Edge Vision & Acoustic Anomaly Detection System (Capstone Project) pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [multimodal_edge_capstone_platform.py](src/multimodal_edge_capstone_platform.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Warden, P. and Situnayake, D., TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers, O Reilly, 2019, [https://www.oreilly.com/library/view/tinyml/9781492052036/](https://www.oreilly.com/library/view/tinyml/9781492052036/) (diperiksa 2026-11-18).
2. Gholami, A. et al., A Survey of Quantization Methods for Efficient Neural Network Inference, IEEE, 2021, [https://arxiv.org/abs/2103.13630](https://arxiv.org/abs/2103.13630) (diperiksa 2026-11-18).
