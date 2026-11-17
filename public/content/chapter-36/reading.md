# Chapter 36: Digital Twins & System Modeling

## Tujuan pembelajaran

Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memahami konsep fundamental **Digital Twin** (Kembaran Digital) dan perbedaannya dengan model CAD 3D statis atau dashboard telemetri biasa.
2. Menganalisis loop sinkronisasi timbal balik dua arah (*bi-directional synchronization*) antara aset fisik (*Physical Twin*) dan representasi komputasi (*Digital Twin*).
3. Mengembangkan model matematika berbasis fisika (*Physics-Based Modeling*) menggunakan persamaan diferensial dinamika termal orde-satu (Hukum Pendinginan Newton & Pemanasan Joule).
4. Menghitung galat residu sinkronisasi (*Residual Drift*) untuk mendeteksi degradasi aset fisik atau kebutuhan kalibrasi parameter model.
5. Menjalankan simulasi skenario prediktif (*What-If Analysis*) untuk memperkirakan perilaku sistem di masa depan tanpa mengambil risiko kerusakan aset fisik nyata.

## Prasyarat

- Pemahaman komunikasi telemetri MQTT dan arsitektur data time-series (Chapter 14 & 25).
- Dasar-dasar persamaan diferensial biasa (ODE) dan metode integrasi numerik Euler.
- Pemrograman Python dasar (pembuatan class berorientasi objek dan manipulasi data deret waktu).

## Konsep dan teori

### 1. Definisi & Taksonomi Digital Twin

Sebuah kembaran digital (*Digital Twin*) didefinisikan sebagai representasi virtual dinamis dari suatu entitas fisik nyata yang terus-menerus disinkronkan melalui aliran data telemetri berkecepatan tinggi:

```
               [Physical Asset]
           (Motor / Ruang Server / Pipa)
             |                      ^
             | Telemetri            | Perintah Aktuasi
             | (Sensor Data)        | (Optimal Setpoints)
             v                      |
+-------------------------------------------------------------+
|                     Digital Twin Core                       |
|   +---------------------+        +----------------------+   |
|   | Dynamic State Sync  | <----> | Physics & Math Model |   |
|   | (Real-Time Shadow)  |        | (First-Principles)   |   |
|   +---------------------+        +----------------------+   |
|                                                              |
|   +---------------------+        +----------------------+   |
|   | Residual Drift Mon. | ---->  | What-If Simulation   |   |
|   | (Anomaly Detection) |        | (Predictive Sandbox) |   |
|   +---------------------+        +----------------------+   |
+-------------------------------------------------------------+
```

Perbedaan kunci Digital Twin:
- **Model CAD Statis**: Hanya menyimpan geometri bentuk tanpa status hidup.
- **Dashboard Telemetri**: Hanya menampilkan riwayat pengukuran pasif tanpa pemahaman hukum fisika internal sistem.
- **Digital Twin**: Menggabungkan data telemetri hidup dengan persamaan fisika sistem untuk memprediksi masa depan (*forecasting*) dan mendiagnosis degradasi (*health index*).

### 2. Model Matematika Dinamika Termal Orde-Satu

Sebagai studi kasus rekayasa, tinjau pemodelan suhu ruang server atau ruang pemanas industri. Laju perubahan suhu terhadap waktu ($\frac{dT}{dt}$) ditentukan oleh keseimbangan energi panas masuk ($Q_{in}$) dan panas yang dibuang ke lingkungan melalui konveksi:

$$\frac{dT}{dt} = \frac{1}{C_{th}} \left( Q_{in} - \frac{T(t) - T_{amb}}{R_{th}} \right)$$

Di mana:
- $T(t)$: Suhu sistem pada waktu $t$ ($^\circ\text{C}$).
- $T_{amb}$: Suhu ambien udara sekitar ($^\circ\text{C}$).
- $Q_{in}$: Daya masukan elemen pemanas dalam satuan Watt ($\text{Joule/detik}$).
- $C_{th}$: Kapasitas termal sistem dalam satuan $\text{Joule/Kelvin}$.
- $R_{th}$: Resistansi termal dinding insulasi dalam satuan $\text{Kelvin/Watt}$.

Menggunakan integrasi numerik Euler dengan langkah waktu diskrit $\Delta t$:

$$T_{k+1} = T_k + \Delta t \cdot \left[ \frac{Q_{in} - \frac{T_k - T_{amb}}{R_{th}}}{C_{th}} \right]$$

### 3. Galat Residu & Kalibrasi Model

Pada kondisi ideal, suhu estimasi digital ($T_{digital}$) akan mengikuti suhu terukur fisik ($T_{physical}$) dengan galat residu sangat kecil:

$$\text{Residual}_k = |T_{physical, k} - T_{digital, k}|$$

Jika $\text{Residual}_k \le \epsilon$ (ambang batas toleransi), model dinyatakan tersinkronisasi (*SYNCHRONIZED*). Namun jika residu terus meningkat melebihi ambang batas, hal ini mengindikasikan:
1. Terjadi kerusakan fisik pada insulasi ruangan (kebocoran udara dingin).
2. Kerusakan sensor (drift kalibrasi ADC).
3. Parameter $R_{th}$ atau $C_{th}$ model perlu dikalibrasi ulang (*Parameter Re-identification*).

### 4. Analisis What-If & Simulasi Prediktif

Keunggulan utama Digital Twin adalah kemampuannya menjadi *sandbox* simulasi tanpa risiko. Operator dapat menguji skenario hipotetis:
- *"Berapa suhu akhir ruangan 60 detik ke depan jika daya pemanas dinaikkan dari 100 Watt ke 250 Watt?"*
- Model digital menjalankan proyeksi ke depan secara instan ($T_{sim}$ naik ke 47.11 $^\circ\text{C}$). Jika suhu tersebut melebihi batas keselamatan perangkat keras, sistem kontrol dapat menolak perintah tersebut sebelum dieksekusi pada mesin fisik nyata.

## Latihan

1. **Analisis Keseimbangan Termal Steady-State**:
   Berdasarkan persamaan diferensial termal di atas, pada kondisi tunak (*steady-state* di mana $\frac{dT}{dt} = 0$), turunkan persamaan suhu maksimum $T_{ss}$ sebagai fungsi dari $Q_{in}$, $R_{th}$, dan $T_{amb}$. Jika $Q_{in} = 250\text{ W}$, $R_{th} = 0.1\text{ K/W}$, dan $T_{amb} = 25^\circ\text{C}$, berapakah suhu tunak sistem?
2. **Pengaruh Langkah Waktu Diskrit ($\Delta t$)**:
   Mengapa pemilihan langkah waktu integrasi numerik $\Delta t$ yang terlalu besar dapat menyebabkan model simulasi mengalami ketidakstabilan (*numerical oscillation/divergence*)? Bagaimana kriteria stabilitas Courant-Friedrichs-Lewy (CFL) berlaku di sini?
3. **Mekanisme Umpan Balik Kalman Filter**:
   Dalam sistem Digital Twin tingkat lanjut, bagaimana algoritma *Extended Kalman Filter (EKF)* menggabungkan data sensor riil yang berderau dengan model fisika teoretis untuk menghasilkan estimasi status state yang optimal?

## Tugas

Kembangkan modul simulasi Digital Twin Python (`digital_twin_sim.py`) yang:
1. Memodelkan sistem termal 1-orde berbasis kapasitas panas $C_{th}$ dan resistansi termal $R_{th}$.
2. Melakukan sinkronisasi langkah-demi-langkah dengan aliran telemetri fisik aktual dan menghitung nilai residu galat secara real-time.
3. Menjalankan simulasi skenario prediktif *What-If* untuk memperkirakan kenaikan suhu sistem saat daya dinaikkan secara ekstrem, membuktikan keselamatan operasional sebelum perintah fisik diterapkan.

## Ringkasan

1. Digital Twin menjembatani dunia fisik dan virtual melalui pertukaran data dua arah dan pemodelan matematika berbasis prinsip fisika pertama.
2. Pemantauan galat residu secara real-time menjadi instrumen efektif untuk mendeteksi degradasi mekanis atau anomali sensor.
3. Fitur simulasi prediktif (*What-If Analysis*) memungkinkan pengujian operasional yang aman, meminimalkan downtime dan mencegah kecelakaan industri.

## Referensi

1. Grieves, M., & Vickers, J. *Digital Twin: Mitigating Unpredictable, Undesirable Emergent Behavior in Complex Systems*. Springer, 2017.
2. Tao, F., et al. *Digital Twin in Industry: State-of-the-Art*. IEEE Transactions on Industrial Informatics, 2019.
3. Incropera, F. P., et al. *Fundamentals of Heat and Mass Transfer*. John Wiley & Sons, 2020.
