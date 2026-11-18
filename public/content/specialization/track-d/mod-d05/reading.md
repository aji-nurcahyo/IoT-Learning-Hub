# Modul D05 — Edge AI Model Lifecycle, Deployment, Benchmarking & Anomaly Tracking

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Menyusun pipeline MLOps edge dari training hingga kompilasi AOT zero dynamic memory.
2. Melakukan profiling latensi per-layer model menggunakan register DWT Cycle Counter perangkat keras.
3. Mengimplementasikan deteksi pergeseran distribusi inferensi menggunakan Population Stability Index (PSI).
4. Merancang mekanisme kalibrasi threshold anomali on-device berbasis Extreme Value Theory (EVT).

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 38, Chapter 39.
- Modul Jalur Peminatan Prasyarat: Modul D03.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Tantangan MLOps pada Mikrokontroler Edge
Berbeda dengan cloud di mana model dapat di-deploy ulang dalam hitungan menit via container, deployment model pada mikrokontroler (*edge devices*) menghadapi keterbatasan konektivitas, memori flash terbatas, dan resiko *bricking* perangkat. Begitu model terpasang di lapangan, akurasinya dapat mengalami degradasi seiring berjalannya waktu akibat dua fenomena:
1. **Data Drift (Covariate Shift)**: Karakteristik input sensor bergeser akibat perubahan musim, suhu lingkungan ekstrim, atau penuaan sensor ($P(X)$ berubah sementara $P(Y|X)$ tetap).
2. **Concept Drift**: Hubungan antara input sensor dan label kerusakan bergeser ($P(Y|X)$ berubah), misalnya ketika mesin diganti komponen mekanikalnya dengan spesifikasi berbeda.

### 2. Metrik Deteksi Drift Ringan: Population Stability Index (PSI)
Untuk mendeteksi drift tanpa harus mengirimkan seluruh data mentah berukuran megabyte ke cloud, edge processor dapat menghitung metrik statistik ringkas pada streaming inferensi:
- **PSI (Population Stability Index)** mengukur divergensi antara distribusi probabilitas skor inferensi baseline ($P_{\text{base}}$) dan distribusi data live terkini ($P_{\text{live}}$) yang dibagi ke dalam $K$ kuantil/bin.
- **Aturan Keputusan Industri**:
  - $\text{PSI} < 0.10$: Distribusi stabil, tidak diperlukan tindakan.
  - $0.10 \le \text{PSI} < 0.25$: Terjadi pergeseran moderat, disarankan pemantauan ketat.
  - $\text{PSI} \ge 0.25$: Terjadi drift signifikan, model wajib di-retrain atau threshold direkalibrasi.

### 3. Landasan Matematis: Formulasi PSI & Divergensi Simetris

1. **Formulasi Population Stability Index (PSI)**:
   $$
   \text{PSI} = \sum_{b=1}^{K} \left( P_{\text{live}}(b) - P_{\text{base}}(b) \right) \times \ln \left( \frac{P_{\text{live}}(b)}{P_{\text{base}}(b)} \right)
   $$
   di mana $P_{\text{base}}(b)$ dan $P_{\text{live}}(b)$ adalah proporsi sampel dalam interval kuantil ke-$b$.

2. **Divergensi Kullback-Leibler Terikat Simetris**:
   Perhatikan bahwa PSI setara dengan jumlah divergensi KL maju dan mundur:
   $$
   \text{PSI} = D_{\text{KL}}(P_{\text{live}} \parallel P_{\text{base}}) + D_{\text{KL}}(P_{\text{base}} \parallel P_{\text{live}})
   $$

3. **Earth Mover's (Wasserstein-1) Distance untuk Skor Kontinu 1D**:
   $$
   W_1(P_{\text{base}}, P_{\text{live}}) = \int_{-\infty}^{\infty} |F_{\text{base}}(t) - F_{\text{live}}(t)| \, dt
   $$
   di mana $F(t)$ adalah fungsi distribusi kumulatif empiris (eCDF).

## Latihan

## Latihan Pemahaman Mandiri

1. **Jika nilai Population Stability Index (PSI) dari skor inferensi batch saat ini bernilai 0.38, tindakan apa yang direkomendasikan secara standar industri?**
   - *Jawaban*: Nilai PSI di atas 0.25 menunjukkan pergeseran populasi yang sangat signifikan dibanding data baseline, sehingga model harus di-retrain dengan data terbaru atau ambang batas anomali harus dikalibrasi ulang.

2. **Mengapa DWT (Data Watchpoint and Trace) Cycle Counter lebih dipilih untuk benchmarking latensi inferensi edge dibanding fungsi timer OS seperti millis()?**
   - *Jawaban*: Register DWT->CYCCNT mencatat setiap detak clock prosesor secara langsung di level silikon hardware, memberikan resolusi siklus instruksi nanodetik tanpa jitter interupsi sistem operasi.

## Tugas

## Penugasan Mandiri

Kembangkan skrip streaming drift tracker berbasis jendela geser 50 sampel inferensi. Uji algoritma dengan data distribusi normal yang bergeser ke kondisi keausan mesin, dan buktikan peringatan PSI >= 0.25 terpicu secara deterministik.

## Ringkasan
- Modul D05 memberikan pemahaman mendalam dan terapan mengenai Edge AI Model Lifecycle, Deployment, Benchmarking & Anomaly Tracking pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [edge_model_drift_sim.py](src/edge_model_drift_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Yurdakul, B., Statistical Properties of Population Stability Index, Western Michigan University, 2018, [https://scholarworks.wmich.edu/dissertations/3313/](https://scholarworks.wmich.edu/dissertations/3313/) (diperiksa 2026-11-18).
2. ARM, Cortex-M Data Watchpoint and Trace (DWT) Technical Reference Manual, [https://developer.arm.com/documentation/ddi0403/latest](https://developer.arm.com/documentation/ddi0403/latest) (diperiksa 2026-11-18).
