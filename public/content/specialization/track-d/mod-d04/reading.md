# Modul D04 — Multimodal Sensor Fusion, Bayesian Estimation & Extended Kalman Filters

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memformulasikan model state-space multi-variat non-linear pada dinamika degradasi mesin.
2. Menurunkan linearisasi deret Taylor matriks Jacobian F(k) dan H(k) untuk sistem fisik nyata.
3. Mengimplementasikan propagasi kovariansi error P dan kalkulasi Kalman Gain optimal pada mikrokontroler.
4. Menerapkan Late Bayesian Fusion berbasis Log-Odds untuk menggabungkan sensor berkecepatan cuplik heterogen.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 05, Chapter 38.
- Modul Jalur Peminatan Prasyarat: Modul D02.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Kebutuhan Fusi Sensor Multimodal pada Mesin Industri
Kegagalan mekanikal dan elektrikal mesin industri tidak pernah tercermin hanya pada satu parameter fisik saja. Kerusakan bantalan menghasilkan pola getaran frekuensi tinggi pada fase awal, diikuti kenaikan temperatur permukaan bearing (*thermal flux*), dan distorsi harmonik arus stator. Mengandalkan sensor tunggal rentan terhadap *false positive* akibat gangguan elektromagnetik (EMI) atau kejutan mekanikal sesaat.

Fusi multimodal memadukan modalitas fisik yang heterogen ke dalam representasi state dinamis terpadu $\mathbf{x}_k$, menghasilkan estimasi kesehatan mesin yang jauh lebih andal dan tahan derau.

### 2. Formulasi State-Space dan Persamaan Non-Linear
Pada sistem fisik nyata, dinamika transisi state dan hubungan antara state terhadap pembacaan sensor bersifat non-linear:
$$
\mathbf{x}_k = f(\mathbf{x}_{k-1}, \mathbf{u}_{k-1}) + \mathbf{w}_{k-1}
$$
$$
\mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}_k
$$
Di mana $\mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q})$ adalah noise proses Gauss dan $\mathbf{v}_k \sim \mathcal{N}(0, \mathbf{R})$ adalah noise pengukuran sensor.

Pada Extended Kalman Filter (EKF), fungsi non-linear $f(\cdot)$ dan $h(\cdot)$ didekati menggunakan ekspansi deret Taylor orde pertama di sekitar estimasi state terkini, menghasilkan matriks Jacobian $\mathbf{F}_k$ dan $\mathbf{H}_k$.

### 3. Landasan Matematis: Propagasi & Pembaruan Kovariansi EKF

1. **Prediksi State dan Kovariansi (Time Update)**:
   $$
   \hat{\mathbf{x}}_k^- = f(\hat{\mathbf{x}}_{k-1}, \mathbf{u}_{k-1})
   $$
   $$
   \mathbf{P}_k^- = \mathbf{F}_k \mathbf{P}_{k-1} \mathbf{F}_k^T + \mathbf{Q}_k
   $$
   di mana matriks Jacobian transisi state adalah:
   $$
   \mathbf{F}_k = \left. \frac{\partial f}{\partial \mathbf{x}} \right|_{\hat{\mathbf{x}}_{k-1}}
   $$

2. **Matriks Jacobian Observasi $\mathbf{H}_k$**:
   $$
   \mathbf{H}_k = \left. \frac{\partial h}{\partial \mathbf{x}} \right|_{\hat{\mathbf{x}}_k^-}
   $$

3. **Inovasi Residual dan Kovariansi Inovasi $\mathbf{S}_k$**:
   $$
   \mathbf{y}_k = \mathbf{z}_k - h(\hat{\mathbf{x}}_k^-)
   $$
   $$
   \mathbf{S}_k = \mathbf{H}_k \mathbf{P}_k^- \mathbf{H}_k^T + \mathbf{R}_k
   $$

4. **Kalman Gain Optimal $\mathbf{K}_k$**:
   $$
   \mathbf{K}_k = \mathbf{P}_k^- \mathbf{H}_k^T \mathbf{S}_k^{-1}
   $$

5. **Pembaruan State dan Kovariansi Posterior (Measurement Update)**:
   $$
   \hat{\mathbf{x}}_k = \hat{\mathbf{x}}_k^- + \mathbf{K}_k \mathbf{y}_k
   $$
   $$
   \mathbf{P}_k = (\mathbf{I} - \mathbf{K}_k \mathbf{H}_k) \mathbf{P}_k^-
   $$

## Latihan

## Latihan Pemahaman Mandiri

1. **Mengapa matriks kovariansi error $P_k$ bernilai menurun setelah langkah Measurement Update pada EKF?**
   - *Jawaban*: Langkah Measurement Update menggunakan informasi sensor $z_k$ untuk mengoreksi state; perkalian $(I - K_k H_k) P_k^-$ secara matematis mereduksi kovariansi error karena kepastian sistem meningkat setelah observasi baru diterima.

2. **Pada Late Bayesian Fusion, apa keuntungan utama menggunakan representasi Log-Odds dibanding perkalian probabilitas langsung?**
   - *Jawaban*: Log-Odds mentransformasikan perkalian probabilitas independen menjadi operasi penjumlahan linier sederhana $\sum \log \Lambda_i$, sangat cepat dihitung pada prosesor integer fixed-point dan kebal terhadap resiko numerical underflow.

## Tugas

## Penugasan Mandiri

Kembangkan skrip Python/C yang menerapkan EKF 4-state pada mikrokontroler untuk mengestimasi keausan bantalan. Fusi harus mampu memitigasi anomali derau transien pada pembacaan sensor getaran tanpa mengalami divergensi kovariansi P.

## Ringkasan
- Modul D04 memberikan pemahaman mendalam dan terapan mengenai Multimodal Sensor Fusion, Bayesian Estimation & Extended Kalman Filters pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [ekf_sensor_fusion_sim.py](src/ekf_sensor_fusion_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Simon, D., Optimal State Estimation: Kalman, H-infinity, and Nonlinear Approaches, Wiley, 2006, [https://www.wiley.com/en-us/Optimal+State+Estimation-p-9780471708582](https://www.wiley.com/en-us/Optimal+State+Estimation-p-9780471708582) (diperiksa 2026-11-18).
2. Bar-Shalom, Y. et al., Estimation with Applications to Tracking and Navigation, Wiley, 2001, [https://www.wiley.com/en-us/Estimation+with+Applications+to+Tracking+and+Navigation-p-9780471416555](https://www.wiley.com/en-us/Estimation+with+Applications+to+Tracking+and+Navigation-p-9780471416555) (diperiksa 2026-11-18).
