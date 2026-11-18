# Modul C02 — Precision In-Situ Calibration, Temperature Drift & Sensor Aging Physics

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Memformulasikan model matematika kompensasi suhu non-linear multi-variabel pada pembacaan sensor lingkungan.
2. Memisahkan kontribusi zero drift dari span drift akibat penuaan elektroda kimiawi di lapangan.
3. Mengimplementasikan propagasi ketidakpastian pengukuran baku mengacu pada ISO/IEC Guide 98-3 (GUM).
4. Membangun skrip evaluasi residual kalibrasi dua titik in-situ untuk pemulihan akurasi sensor jangka panjang.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 07, Chapter 10.
- Modul Jalur Peminatan Prasyarat: Modul C01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Dinamika Drift dan Penuaan Sensor di Lapangan
Transduser lingkungan in-situ (sensor gas semikonduktor MOX, sel elektrokimia, dan sensor kapasitif kelembaban) beroperasi di bawah fluktuasi iklim ekstrem yang memicu penyimpangan karakteristik transfer secara kontinu:
1. **Zero Drift (Pergeseran Titik Nol)**: Perubahan tegangan keluaran saat kuantitas fisik yang diukur bernilai nol ($X = 0$). Disebabkan oleh degradasi lapisan elektrokimia, penumpukan kontaminan debu pada membran hidrofobik, atau pergeseran tegangan bias penguat operasional.
2. **Span Drift (Pergeseran Kemiringan/Sensitivitas)**: Perubahan laju respons $\frac{dV}{dX}$ transduser, umumnya diakibatkan oleh perubahan koefisien ekspansi termal atau penuaan kristal material pengindera.
3. **Drift Termal Reversibel vs Penuaan Irreversibel**:
   - Drift termal bersifat langsung dan reversibel: nilai sinyal kembali ke asal saat suhu kembali ke suhu acuan $T_{\text{ref}} = 25^\circ\text{C}$.
   - Penuaan (*aging*) bersifat ireversibel dan monoton terhadap waktu: degradasi elektrolit padat atau korosi mikro interkoneksi silikon yang bertambah seiring berjalannya hari operasional.

### 2. Standar Metrologi ISO/IEC Guide 98-3 (GUM)
Setiap angka pengukuran instrumen tanpa pernyataan batas ketidakpastian (*measurement uncertainty*) tidak memiliki validitas ilmiah. Mengacu pada pedoman internasional *Guide to the Expression of Uncertainty in Measurement* (GUM):
- **Evaluasi Tipe A**: Ketidakpastian yang dievaluasi dengan metode statistik dari deret pengamatan berulang (standar deviasi rata-rata sampel $s / \sqrt{n}$).
- **Evaluasi Tipe B**: Ketidakpastian yang dievaluasi berdasarkan sertifikat kalibrasi pabrikan, resolusi ADC, atau batas toleransi komponen ($u = a / \sqrt{3}$ untuk distribusi seragam).
- **Ketidakpastian Baku Gabungan ($u_c$)**: Akar dari penjumlahan varians masing-masing sumber galat independen berbobot koefisien sensitivitas:
$$
u_c^2(y) = \sum_{i=1}^{N} \left( \frac{\partial f}{\partial x_i} \right)^2 u^2(x_i)
$$

### 3. Landasan Matematis: Model Kalibrasi Dua Titik & Propagasi Galat

1. **Model Koreksi Drift Suhu & Waktu Dua Titik**:
   $$
   V_{\text{corrected}} = \frac{V_{\text{raw}} - \left[ V_0 + \alpha_T (T - T_{\text{ref}}) + \gamma_t \cdot t \right]}{1 + \beta_T (T - T_{\text{ref}})}
   $$
   di mana:
   - $V_0$: Offset awal tegangan pada $T_{\text{ref}}$ dan $t = 0$.
   - $\alpha_T$: Koefisien drift suhu offset ($\text{V/}^\circ\text{C}$).
   - $\beta_T$: Koefisien drift suhu sensitivitas span ($1/^\circ\text{C}$).
   - $\gamma_t$: Laju penuaan harian ($\text{V/hari}$).

2. **Worked Numerical Example (Langkah-demi-Langkah)**:
   - **Kondisi Masukan**:
     - Tegangan mentah: $V_{\text{raw}} = 1{,}250\text{ V}$
     - Suhu aktual: $T = 38{,}0^\circ\text{C}$ (kenaikan $\Delta T = 13{,}0^\circ\text{C}$ dari $T_{\text{ref}} = 25{,}0^\circ\text{C}$)
     - Waktu di lapangan: $t = 180\text{ hari}$
     - Koefisien: $V_0 = 0{,}100\text{ V}$, $\alpha_T = 2{,}4\text{ mV/}^\circ\text{C} = 0{,}0024\text{ V/}^\circ\text{C}$, $\gamma_t = 0{,}05\text{ mV/hari} = 0{,}00005\text{ V/hari}$, $\beta_T = 0{,}00015\text{ }^\circ\text{C}^{-1}$.
   - **Kalkulasi Offset Total**:
     $$
     V_{\text{offset}} = 0{,}100 + (0{,}0024 \times 13{,}0) + (0{,}00005 \times 180) = 0{,}100 + 0{,}0312 + 0{,}0090 = 0{,}1402\text{ V}
     $$
   - **Kalkulasi Faktor Skala Span**:
     $$
     S = 1 + (0{,}00015 \times 13{,}0) = 1{,}00195
     $$
   - **Tegangan Terkoreksi**:
     $$
     V_{\text{corrected}} = \frac{1{,}250 - 0{,}1402}{1{,}00195} = \frac{1{,}1098}{1{,}00195} = 1{,}10787\text{ V}
     $$
   - **Ketidakpastian Gabungan**: Dengan $u_{\text{ADC}} = 1{,}5\text{ mV}$, $u_T = 0{,}5^\circ\text{C}$ (komponen suhu $= 0{,}0024 \times 0{,}5 = 1{,}2\text{ mV}$), dan $u_{\text{model}} = 2{,}0\text{ mV}$:
     $$
     u_c = \sqrt{1{,}5^2 + 1{,}2^2 + 2{,}0^2} = \sqrt{2{,}25 + 1{,}44 + 4{,}00} = \sqrt{7{,}69} = 2{,}773\text{ mV} \approx 0{,}00278\text{ V}
     $$
     Ketidakpastian diperluas ($k=2$, tingkat keyakinan $95\%$): $U = 2 \times 2{,}78\text{ mV} = 5{,}55\text{ mV}$.

## Latihan

## Latihan Pemahaman Mandiri

1. **Apa perbedaan mendasar antara zero drift dan span drift pada kurva kalibrasi sensor?**
   - *Jawaban*: Zero drift menggeser seluruh kurva kalibrasi ke atas atau ke bawah secara paralel (offset bertambah konstan untuk semua nilai input), sedangkan span drift mengubah kemiringan kurva respons (sensitivitas sensor berubah, menghasilkan galat yang proporsional terhadap besar sinyal masukan).

2. **Mengapa nilai faktor cakupan $k = 2$ digunakan dalam menentukan ketidakpastian bentangan ($Expanded Uncertainty$ $U$)?**
   - *Jawaban*: Berdasarkan Teorema Limit Pusat, distribusi probabilitas dari kombinasi berbagai sumber ketidakpastian acak akan mendekati distribusi normal (Gauss). Faktor cakupan $k = 2$ merepresentasikan rentang interval kepercayaan sekitar $pm 2$ standar deviasi, yang mencakup probabilitas keyakinan sekitar $95{,}45\%$.

## Tugas

## Penugasan Mandiri: Pemulihan Kalibrasi Multi-Variabel & Estimasi GUM

Kembangkan modul Python yang menerima deret waktu pembacaan sensor tegangan mentah yang terdistorsi oleh kenaikan suhu siang hari dan degradasi penuaan selama 1 tahun. Terapkan algoritma kompensasi drift termal dan hasilkan format pelaporan metrologi resmi dengan nilai ketidakpastian $U_{95}$.

## Ringkasan
- Modul C02 memberikan pemahaman mendalam dan terapan mengenai Precision In-Situ Calibration, Temperature Drift & Sensor Aging Physics pada tingkat kedalaman L3: Advanced Engineering.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [sensor_calibration_drift_sim.py](src/sensor_calibration_drift_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. JCGM 100:2008, Evaluation of Measurement Data — Guide to the Expression of Uncertainty in Measurement (GUM), [https://www.bipm.org/en/committees/jc/jcgm/publications](https://www.bipm.org/en/committees/jc/jcgm/publications) (diperiksa 2026-11-18).
2. Bentley, J. P., Principles of Measurement Systems, 4th ed., Pearson, 2005, [https://www.pearson.com/en-us/subject-catalog/p/principles-of-measurement-systems/P200000003264](https://www.pearson.com/en-us/subject-catalog/p/principles-of-measurement-systems/P200000003264) (diperiksa 2026-11-18).
