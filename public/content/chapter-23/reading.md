# Chapter 23 — Edge Processing & Local Automation

Mengalirkan seluruh data sensor mentah (*raw data*) langsung ke cloud adalah pendekatan yang tidak efisien dan berbahaya bagi sistem berskala industri. Ketika frekuensi sampling tinggi (misal: $10\text{–}100\text{ Hz}$), biaya transfer bandwidth melonjak, penyimpanan cloud membengkak, dan latensi jaringan dapat memicu kegagalan aktuasi kritis. Terlebih lagi, ketergantungan penuh pada cloud menyebabkan fasilitas industri lumpuh total saat koneksi internet terputus.

**Edge Processing** mentransformasikan gateway lokal dari sekadar pipa penerus data pasif menjadi simpul komputasi cerdas. Bab ini membahas implementasi algoritma pemfilteran anomali statistik (*IQR filter*), kompresi berbasis perubahan (*deadband filtering*), kalkulasi statistik jendela waktu geser (*sliding window*), mesin aturan otomasi mandiri dengan kontrol histeresis, serta sinkronisasi antrean *spool buffer* ke cloud tanpa risiko kehilangan data (*store-and-forward*).

![Alur Pemrosesan Edge: Conditioning, Agregasi, Mesin Aturan Lokal, dan Sinkronisasi](content/chapter-23/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Menganalisis Trade-off Edge vs Cloud**: Membandingkan implikasi teknis dan ekonomis antara pemrosesan lokal di edge dengan komputasi tersentralisasi di cloud (latensi, bandwidth, ketersediaan jaringan, dan privasi).
2. **Menerapkan Algoritma Pemfilteran Derau**: Mengimplementasikan filter statistik *Interquartile Range (IQR)* untuk mengeliminasi lonjakan liar (*spike*) dan *deadband thresholding* untuk mereduksi transmisi data statis.
3. **Merancang Agregasi Jendela Waktu**: Menghitung ringkasan statistik (rata-rata, deviasi standar, nilai minimum, dan maksimum) menggunakan teknik *Tumbling* dan *Sliding Window*.
4. **Membangun Mesin Aturan Lokal (*Local Rule Engine*)**: Mengembangkan logika kontrol aktuasi berbasis histeresis yang bekerja secara deterministik di tepi jaringan tanpa ketergantungan koneksi internet (*local fail-safe*).
5. **Mengelola Buffer Sinkronisasi (*Store-and-Forward*)**: Mengimplementasikan antrean memori lokal yang menampung data saat tautan internet putus dan mengurasnya (*drain batch*) secara teratur ketika koneksi pulih kembali.

## Prasyarat

- Memahami arsitektur gateway Linux dari [Chapter 22](chapter-22).
- Memahami struktur data model dan format telemetri dari [Chapter 21](chapter-21).
- Memahami konsep dasar statistik deskriptif (kuartil, rata-rata aritmatika, dan varians).

## Konsep dan teori

### 1. Motivasi Komputasi Edge

Komputasi edge menyelesaikan empat kendala utama sistem IoT terpusat:

1. **Latensi Deterministik**: Siklus keputusan di tepi jaringan membutuhkan waktu $< 5\text{ ms}$, sedangkan panggilan API cloud membutuhkan waktu $100\text{–}500\text{ ms}$ (tidak cocok untuk sistem darurat atau *safety trip*).
2. **Penghematan Bandwidth**: Mengirimkan rata-rata per menit alih-alih pembacaan $10\text{ Hz}$ memangkas konsumsi data hingga $>98\%$.
3. **Operasi Mandiri (*Offline Resilience*)**: Otomasi ventilasi atau pendinginan server tetap berjalan normal saat kabel serat optik penyedia internet terputus.
4. **Kepatuhan Privasi**: Data mentah sensitif disaring dan dianonimkan di gerbang sebelum diunggah ke pihak ketiga.

### 2. Algoritma Pemfilteran Statistik (IQR & Deadband)

Sensor fisik kerap mengalami lonjakan anomali sesaat akibat gangguan induksi elektromagnetik atau fluktuasi pasokan daya.

#### A. Filter Interquartile Range (IQR)
Menghitung selisih antara kuartil ketiga ($Q_3$) dan kuartil pertama ($Q_1$):

$$\text{IQR} = Q_3 - Q_1$$

Data diklasifikasikan sebagai nilai valid jika dan hanya jika berada dalam batas:

$$Q_1 - k \cdot \text{IQR} \le x_i \le Q_3 + k \cdot \text{IQR}$$

Di mana konstanta $k = 1{,}5$ merupakan standar statistik Tukey untuk menyaring *mild outliers*.

#### B. Filter Deadband (Peredam Fluktuasi Statis)
Mencegah transmisi paket jika perubahan nilai terhadap nilai sebelumnya ($\Delta x$) lebih kecil dari ambang batas toleransi ($\delta$):

$$\text{Kirim jika: } |x_{\text{baru}} - x_{\text{terakhir}}| \ge \delta$$

### 3. Agregasi Jendela Waktu (Windowing)

Terdapat dua model utama pengelompokan data beruntun waktu:

1. **Tumbling Window (Jendela Lepas)**: Jendela waktu berurutan tanpa tumpang tindih (misal: agregasi tiap interval $60\text{ detik}$ diskrit).
2. **Sliding / Hopping Window (Jendela Geser)**: Jendela berukuran tetap ($N$ sampel atau $T$ detik) yang bergeser setiap kali ada sampel baru masuk, menghasilkan nilai rata-rata bergerak (*moving average*).

Rata-rata bergerak ($\mu$) dan varians ($\sigma^2$) dihitung dari subset data yang telah disaring:

$$\mu = \frac{1}{N} \sum_{i=1}^{N} x_i, \quad \sigma = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2}$$

### 4. Kontrol Histeresis Mesin Aturan Lokal

Jika aktuator (seperti relay kompresor pendingin) dihidupkan tepat pada ambang $T \ge 30{,}0\,^\circ\text{C}$ dan dimatikan saat $T < 30{,}0\,^\circ\text{C}$, osilasi suhu di sekitar $30{,}0\,^\circ\text{C}$ akan menyebabkan relay menyala dan mati puluhan kali per menit (*relay chattering*), yang cepat merusak kontak mekanis kontaktor.

**Kontrol Histeresis** menetapkan dua ambang batas yang berbeda:
- **Ambang Batas Atas ($T_{\text{high}}$)**: Relay aktif saat $T \ge T_{\text{high}}$ ($30{,}0\,^\circ\text{C}$).
- **Ambang Batas Bawah ($T_{\text{low}} = T_{\text{high}} - H$)**: Relay mati **hanya jika** suhu turun di bawah $T_{\text{low}}$ ($28{,}5\,^\circ\text{C}$ untuk pita histeresis $H = 1{,}5\,^\circ\text{C}$).

### 5. Arsitektur Buffer Spooling (Store-and-Forward)

Ketika gateway mendeteksi tautan cloud offline:
1. Data telemetri agregat dialihkan ke antrean memori lokal atau basis data lokal (`EdgeSpoolBuffer`).
2. Terapkan kebijakan *Drop-Oldest* jika kapasitas batas memori terancam terlampaui.
3. Saat koneksi cloud terdeteksi pulih, data dikuras secara bertahap (*batch drain*, misal $10\text{ paket}$ per transaksi) agar tidak membanjiri buffer transmisi soket TCP.

## Latihan

1. **Kalkulasi IQR**:
   Diberikan 8 pembacaan suhu berurutan (dalam $^\circ\text{C}$):
   `[24.0, 24.2, 24.1, 85.0, 24.3, 24.2, -30.0, 24.4]`
   Hitung $Q_1$, $Q_3$, dan $\text{IQR}$. Tentukan apakah nilai $85{,}0$ dan $-30{,}0$ masuk dalam kategori outlier menurut batas $k = 1{,}5$.
2. **Analisis Histeresis vs Chattering**:
   Sebuah sistem ventilasi memiliki ambang batas panas $32{,}0\,^\circ\text{C}$ tanpa histeresis. Jika profil suhu ruangan bergerak $31{,}9 \rightarrow 32{,}1 \rightarrow 31{,}9 \rightarrow 32{,}1 \rightarrow 31{,}9\,^\circ\text{C}$ dalam waktu 10 detik, berapa kali sakelar relay berpindah posisi? Bandingkan dengan sistem yang menggunakan pita histeresis $1{,}0\,^\circ\text{C}$.
3. **Manajemen Buffer Offline**:
   Jika sebuah edge gateway menghasilkan paket agregat setiap $10\text{ detik}$ ($6\text{ paket/menit}$) dengan kapasitas antrean RAM $1000\text{ paket}$, berapa lama waktu maksimal jaringan internet boleh mati sebelum paket tertua mulai terbuang (*drop-oldest*)?

## Tugas

Rancang dan bangun mesin pemrosesan edge mandiri menggunakan Python:

1. **Implementasi Modul Filter**:
   Bangun fungsi filter IQR untuk mengeliminasi lonjakan eksternal dan kelas `DeadbandFilter` untuk menahan transmisi perubahan nilai di bawah $0{,}5\,^\circ\text{C}$.
2. **Modul Agregasi Sliding Window**:
   Susun kelas `SlidingWindowAggregator` yang menghitung metrik agregat (jumlah sampel bersih, rata-rata, nilai min/max, deviasi standar) dari jendela $N = 5$ sampel.
3. **Mesin Aturan Histeresis**:
   Implementasikan kelas `LocalAutomationEngine` dengan ambang batas atas $30{,}0\,^\circ\text{C}$ dan pita histeresis $1{,}5\,^\circ\text{C}$. Buktikan melalui pengujian simulasi bahwa tidak terjadi perpindahan relay saat suhu berfluktuasi di dalam pita histeresis.
4. **Buffer Sinkronisasi Cloud**:
   Bangun mekanisme *spool buffer* dengan batas kapasitas $10\text{ slot}$ dan buktikan pengurasan bertahap (*batch draining*) saat status kembali online.

### Rubrik Penilaian

| Kriteria | Bobot | Deskripsi Teknis |
| :--- | :---: | :--- |
| **Pemfilteran Outlier & Deadband** | 35% | Filter IQR dan deadband berfungsi akurat; sampel ekstrim berhasil disingkirkan tanpa merusak urutan sampel valid. |
| **Agregasi Window & Mesin Aturan Histeresis** | 35% | Kalkulasi statistik moving average benar; mesin aturan mencegah chattering relay secara deterministik pada pengujian profil suhu. |
| **Store-and-Forward Spooling & Arsitektur** | 30% | Buffer menangani kondisi offline dengan prinsip drop-oldest dan mampu menguras batch secara bertahap saat pulih; dokumentasi lengkap. |

## Ringkasan

1. **Reduksi Beban Cloud**: Edge processing memangkas kebutuhan bandwidth dan biaya penyimpanan cloud melalui pemfilteran dan agregasi di gerbang lokal.
2. **Eliminasi Derau**: Filter statistik IQR efektif membuang anomali instan, sementara deadband mengeliminasi pengiriman data statis berulang.
3. **Kontrol Mandiri Berkelanjutan**: Mesin aturan histeresis menjamin kestabilan aktuator mekanis dan memastikan sistem tetap berfungsi aman saat internet padam.
4. **Store-and-Forward**: Mekanisme spool buffer menjamin kontinuitas data historis tanpa kehilangan rekaman saat terjadi gangguan koneksi uplink.

## Referensi

1. Mahdavinejad, M. S., et al. *Machine learning for Internet of Things data analysis: A survey*. Digital Communications and Networks, 4(3), 161-175.
2. Tukey, J. W. *Exploratory Data Analysis*. Addison-Wesley Publishing Company.
3. Franklin, G. F., Powell, J. D., & Workman, M. L. *Digital Control of Dynamic Systems*. Chapter: Nonlinear Control and Hysteresis.
