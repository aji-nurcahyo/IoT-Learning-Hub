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

### 5. Landasan Matematis: Analisis Solusi Analitis vs Numerik & Syarat Stabilitas Euler (Mathematical Foundations)

Persamaan diferensial dinamika termal orde-satu memiliki solusi eksak analitis pada kondisi input daya konstan $Q_{\text{in}}$ dari kondisi awal $T(0) = T_0$:
$$
T(t) = T_{\text{amb}} + Q_{\text{in}} R_{\text{th}} + \left( T_0 - T_{\text{amb}} - Q_{\text{in}} R_{\text{th}} \right) e^{-t / \tau}
$$
di mana $\tau = R_{\text{th}} C_{\text{th}}$ adalah konstanta waktu termal sistem (dalam satuan detik).
Saat $t \to \infty$, suku eksponensial meluruh mendekati nol, menghasilkan suhu tunak (*steady-state temperature*):
$$
T_{\text{ss}} = T_{\text{amb}} + Q_{\text{in}} R_{\text{th}}
$$

**Syarat Batas Stabilitas Integrasi Numerik Euler**:
Dalam metode Forward Euler, galat lokal pemotongan berorde $O(\Delta t)$. Agar integrasi numerik stabil tanpa osilasi tak hingga, langkah waktu diskrit $\Delta t$ wajib memenuhi kriteria stabilitas:
$$
\left| 1 - \frac{\Delta t}{R_{\text{th}} C_{\text{th}}} \right| < 1 \implies 0 < \Delta t < 2 R_{\text{th}} C_{\text{th}} = 2\tau
$$
Untuk menghindari osilasi palsu disyaratkan $\Delta t \le \tau$. Jika $\tau = 50\text{ s}$, maka langkah simulasi $\Delta t = 1{,}0\text{ s}$ menjamin konvergensi numerik yang sangat presisi dengan galat pemotongan terabaikan.

**Worked Numerical Example (What-If Projection & Kalibrasi Residu)**:
Sebuah ruang baterai memiliki parameter $C_{\text{th}} = 500\text{ J/K}$ dan $R_{\text{th}} = 0{,}10\text{ K/W}$ (sehingga $\tau = 50\text{ detik}$). Suhu awal sistem setara suhu ambien $T_0 = T_{\text{amb}} = 25{,}0\,^\circ\text{C}$.
1. Sistem diberi daya disipasi panas $Q_{\text{in}} = 200\text{ Watt}$. Suhu tunak teoritis adalah:
   $$
   T_{\text{ss}} = 25{,}0 + (200 \times 0{,}10) = 25{,}0 + 20{,}0 = 45{,}0\,^\circ\text{C}
   $$
2. Proyeksi suhu pada $t = 30\text{ detik}$ di masa depan:
   $$
   T(30) = 45{,}0 + (25{,}0 - 45{,}0) e^{-30 / 50} = 45{,}0 - 20{,}0 \cdot e^{-0{,}6}
   $$
   Karena $e^{-0{,}6} \approx 0{,}5488$:
   $$
   T(30) = 45{,}0 - (20{,}0 \times 0{,}5488) = 45{,}0 - 10{,}976 = 34{,}024\,^\circ\text{C}
   $$
3. Jika pada detik ke-30 sensor fisik telemetri melaporkan suhu aktual $T_{\text{physical}} = 38{,}50\,^\circ\text{C}$, maka galat residu sinkronisasi adalah:
   $$
   \text{Residual} = |38{,}50 - 34{,}024| = 4{,}476\,^\circ\text{C}
   $$
   Jika ambang toleransi residu normal diatur $\epsilon = 1{,}5\,^\circ\text{C}$, nilai residu $4{,}48\,^\circ\text{C}$ memicu deteksi dini degradasi sistem pendingin (misal kipas radiator macet) bahkan sebelum suhu mencapai batas bahaya absolut $50\,^\circ\text{C}$.

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
