# Chapter 26 — Dashboards, Visualization & Alerting

Data deret waktu yang tersimpan di basis data tidak memiliki nilai operasional jika operator tidak dapat mengamati kondisi sistem secara intuitif dan merespons anomali secara tepat waktu. Namun, menyajikan visualisasi data IoT bukanlah sekadar menampilkan grafik warna-warni yang ramai. Di ruang kendali industri (*Control Room*), kepadatan visual yang buruk dan notifikasi peringatan yang terus-menerus berbunyi palsu (*alert noise*) menyebabkan fenomena fatal yang dikenal sebagai **Alert Fatigue**, di mana teknisi menjadi kebal atau sengaja mengabaikan alarm darurat yang berujung pada bencana operasional.

Bab ini membahas perancangan arsitektur visualisasi profesional menggunakan **Grafana**, pemilihan tipe panel representatif (*Stat KPI, Gauge, Time-Series Graph*), metrik kesehatan armada (*Fleet Availability, MTBF, PDR*), serta siklus hidup mesin status peringatan (*Alert State Machine*) lengkap dengan durasi penahanan *Pending* ($T_{\text{for}}$), pelepasan histeresis anti-flapping, dan pembatasan laju notifikasi (*notification throttling*).

![Arsitektur Visualisasi Dashboard dan Siklus Hidup Peringatan Alert State Machine](content/chapter-26/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Merancang Hierarki Visualisasi Dashboard**: Mengorganisasikan panel dashboard berdasarkan tingkat prioritas operasional (KPI agregat tingkat tinggi di atas, grafik tren deret waktu di tengah, dan log diagnostik di bawah).
2. **Memilih Komponen Visualisasi yang Tepat**: Menentukan penggunaan *Stat Panel* untuk ringkasan numerik tunggal, *Gauge* untuk status seketika terhadap ambang batas fisik, dan *Time-Series Graph* untuk analisis tren historis.
3. **Mengukur Metrik Kinerja Armada (IoT KPIs)**: Menghitung metrik ketersediaan (*Fleet Availability*), *Packet Delivery Ratio (PDR)*, *Mean Time Between Failures (MTBF)*, dan *Mean Time To Detect/Resolve (MTTD/MTTR)*.
4. **Menerapkan Alert State Machine**: Membangun mesin status peringatan 4-tahap (`NORMAL` $\rightarrow$ `PENDING` $\rightarrow$ `FIRING` $\rightarrow$ `RESOLVED`) untuk mengeliminasi alarm palsu dari lonjakan data sesaat (*transient noise*).
5. **Mencegah Fenomena Alert Fatigue & Flapping**: Menerapkan pita histeresis pelepasan alarm, agregasi insiden, pengelompokan tingkat keparahan (*P1/Critical*, *P2/Warning*, *P3/Info*), dan interval pembatasan (*throttling*).

## Prasyarat

- Memahami arsitektur penyimpanan deret waktu dan downsampling dari [Chapter 25](chapter-25).
- Memahami konsep ambang batas kendali dan histeresis dari [Chapter 23](chapter-23).
- Memahami taksonomi pesan dan tingkat keparahan event dari [Chapter 21](chapter-21).

## Konsep dan teori

### 1. Prinsip Desain Dashboard Industri

Sebuah dashboard yang efektif mengikuti prinsip **Situational Awareness**:
- **3-Second Rule**: Dalam 3 detik pertama melirik layar, operator harus langsung mengetahui apakah seluruh sistem berada dalam status normal atau ada simpul yang kritis.
- **Konsistensi Skema Warna Fungsional**:
  - Hijau: Normal / Operasional optimal.
  - Oranye / Kuning: Peringatan awal (*Warning*) / Mendekati ambang batas.
  - Merah: Kondisi Kritis (*Critical Incident*) / Perlu tindakan segera.
  - Abu-abu / Biru: Perangkat mati (*Offline*) atau status netral.
- **Hindari AI Slop Visual**: Hindari animasi berlebihan, gradasi neon mengambang yang menyilaukan mata, atau kartu informasi bersarang (*nested cards*) tanpa tujuan fungsional yang jelas.

### 2. Key Performance Indicators (KPI) Armada IoT

Empat metrik utama untuk mengevaluasi keandalan jaringan perangkat terhubung:

1. **Fleet Availability ($A$)**:
   Persentase simpul yang aktif berkomunikasi dalam jendela waktu evaluasi terhadap total inventaris:
   $$A = \frac{N_{\text{online}}}{N_{\text{total}}} \times 100\%$$
2. **Packet Delivery Ratio (PDR)**:
   Rasio antara jumlah paket yang sukses diterima broker terhadap total paket yang dipancarkan simpul sensor:
   $$\text{PDR} = \frac{\sum \text{Packets Received}}{\sum \text{Packets Sent}} \times 100\%$$
3. **Mean Time Between Failures (MTBF)**:
   Rata-rata waktu operasional normal antara dua kejadian kegagalan beruntun:
   $$\text{MTBF} = \frac{\text{Total Waktu Operasional Normal}}{\text{Jumlah Kejadian Gangguan}}$$
4. **Mean Time To Detect (MTTD) & Resolve (MTTR)**:
   Waktu rata-rata yang dibutuhkan sistem untuk mendeteksi anomali sejak kejadian fisik terjadi, dan durasi yang dibutuhkan teknisi untuk memulihkan kondisi sistem.

### 3. Siklus Hidup Peringatan (Alert State Machine)

Pemicuan alarm sederhana berbasis ambang instan (`if temp > 30: send_sms()`) adalah kesalahan desain fatal yang membanjiri ponsel operator dengan ratusan pesan saat sensor mengalami derau sesaat.

Standar mesin peringatan industri (seperti pada **Prometheus Alertmanager** atau **Grafana Alerting**) menerapkan siklus 4-tahap:

$$\text{NORMAL} \xrightarrow{\text{val} \ge T_{\text{high}}} \text{PENDING} \xrightarrow{\Delta t \ge T_{\text{for}}} \text{FIRING} \xrightarrow{\text{val} < T_{\text{clear}}} \text{RESOLVED}$$

1. **NORMAL**: Parameter lingkungan berada di dalam rentang aman. Tidak ada aksi yang diambil.
2. **PENDING**: Nilai sensor melampaui batas $T_{\text{high}}$, tetapi belum tentu anomali permanen. Sistem memulai pewaktu durasi $T_{\text{for}}$ (misal $5\text{ detik}$ atau $5\text{ menit}$). Jika nilai kembali turun sebelum $T_{\text{for}}$ terpenuhi, status kembali ke `NORMAL` tanpa pernah mengganggu operator (*transient spike rejection*).
3. **FIRING**: Nilai anomali bertahan melebihi $T_{\text{for}}$. Status resmi menjadi insiden aktif, dan pesan peringatan dipancarkan ke saluran komunikasi operator.
4. **RESOLVED**: Nilai sensor turun melewati ambang batas pemulihan $T_{\text{clear}}$. Notifikasi penyelesaian dikirimkan, dan status kembali ke `NORMAL`.

### 4. Mitigasi Alert Flapping Menggunakan Histeresis

Jika suhu ruangan pendingin berosilasi cepat di sekitar $30{,}0\,^\circ\text{C}$ ($29{,}9 \rightarrow 30{,}1 \rightarrow 29{,}9 \rightarrow 30{,}1\,^\circ\text{C}$), alarm akan berganti status antara `NORMAL` dan `FIRING` berulang kali (*alert flapping*).

Untuk mencegahnya, sistem menerapkan **Pita Histeresis ($H$)**:
- Alarm memicu `FIRING` pada: $T_{\text{high}} = 30{,}0\,^\circ\text{C}$.
- Alarm hanya dianggap `RESOLVED` jika suhu turun melewati batas:
  $$T_{\text{clear}} = T_{\text{high}} - H$$
  Dengan $H = 1{,}0\,^\circ\text{C}$, sistem tidak akan mengirim notifikasi *Resolved* hingga suhu menyentuh $< 29{,}0\,^\circ\text{C}$.

### 5. Strategi Anti-Alert Fatigue

1. **Notification Throttling / Rate Limiting**: Membatasi interval pengiriman pengingat ulang (misal: pengingat insiden yang sama hanya boleh dikirim kembali setelah jeda $15\text{ menit}$).
2. **Stratifikasi Saluran Komunikasi**:
   - **P1 (Kritis / Bahaya Nyata)**: Pager / Telepon / Sirene lokal / SMS darurat.
   - **P2 (Peringatan / Degradasi Performa)**: Notifikasi grup Slack / Microsoft Teams / Email operasional.
   - **P3 (Informasi / Diagnostik Rutin)**: Pencatatan ke log internal dashboard tanpa mengaktifkan bunyi alarm.

## Latihan

1. **Analisis Transient Spike**:
   Sebuah sensor suhu mendeteksi lonjakan sesaat ke $45\,^\circ\text{C}$ selama 2 detik akibat induksi elektromagnetik mesin las, lalu segera kembali ke $26\,^\circ\text{C}$. Jelaskan bagaimana konfigurasi durasi $T_{\text{for}} = 10\text{ detik}$ pada status `PENDING` berhasil mencegah terjadinya kepanikan operator di ruang kontrol.
2. **Kalkulasi Metrik Ketersediaan Armada**:
   Sebuah jaringan penerangan jalan pintar memiliki 500 unit lampu LED cerdas. Pada evaluasi harian, rata-rata terdapat 15 unit lampu yang tidak mengirimkan telemetri status selama 24 jam penuh. Hitung nilai *Fleet Availability* ($A$) jaringan tersebut.
3. **Pemberantasan Alert Flapping**:
   Sebuah tangki air memiliki sensor level yang memicu alarm banjir pada batas $80\%$. Tentukan nilai ambang pembersihan (*clear threshold*) yang ideal jika Anda menerapkan pita histeresis $5\%$, dan jelaskan mengapa tangki harus surut hingga batas tersebut sebelum status dinyatakan aman kembali.

## Tugas

Rancang dan validasi model dashboard pemantauan lingkungan serta mesin status peringatan menggunakan Python:

1. **Model Konfigurasi Dashboard Grafana**:
   Susun model deklaratif JSON [`grafana_dashboard_model.json`](content/chapter-26/src/grafana_dashboard_model.json) yang memuat panel Stat KPI (Kesehatan Armada, PDR), panel Gauge (Suhu Langsung dengan pita warna), dan panel Time-Series Graph (Tren suhu 24 jam dari rollup 1 menit).
2. **Implementasi Alert State Machine**:
   Bangun kelas `AlertRule` pada [`alert_state_machine.py`](content/chapter-26/src/alert_state_machine.py) yang mengimplementasikan transisi empat status (`NORMAL`, `PENDING`, `FIRING`, `RESOLVED`).
3. **Verifikasi Durasi Penahanan ($T_{\text{for}}$)**:
   Buktikan bahwa lonjakan suhu yang berlangsung kurang dari durasi $T_{\text{for}} = 5\text{ detik}$ tidak akan memicu notifikasi peringatan.
4. **Verifikasi Histeresis & Throttling**:
   Buktikan bahwa ketika status sedang `FIRING`, fluktuasi kecil tidak memicu pemulihan sebelum menyentuh batas aman $T_{\text{high}} - H$, serta pengingat berkala dibatasi oleh interval *throttle*.

### Rubrik Penilaian

| Kriteria | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Desain Panel Dashboard & Metrik KPI** | 35% | Model dashboard mematuhi prinsip hierarki visual; pemilihan tipe panel dan konfigurasi ambang batas warna tepat. |
| **Akurasi Alert State Machine & Histeresis** | 35% | Siklus 4-tahap berjalan akurat; durasi penahanan $T_{\text{for}}$ dan pita histeresis terbukti efektif mencegah flapping alarm. |
| **Mitigasi Alert Fatigue & Pengujian Deterministik** | 30% | Logika notification throttling berhasil meredam spam pesan; seluruh 10 skenario pengujian timeline lulus verifikasi. |

## Ringkasan

1. **Visualisasi Fungsional**: Dashboard industri dirancang untuk menyajikan kesadaran situasional dalam 3 detik, bukan sekadar hiasan grafis.
2. **Pengukuran Terukur**: Metrik KPI seperti Availability, PDR, dan MTBF memberikan gambaran objektif terhadap kesehatan infrastruktur IoT.
3. **Filosofi Alert State Machine**: Transisi melalui status `PENDING` dengan durasi $T_{\text{for}}$ adalah kunci utama meredam alarm palsu dari derau transien.
4. **Anti-Fatigue**: Mengombinasikan histeresis ambang batas dan pembatasan laju pengiriman (*throttling*) melindungi operator dari kepenatan alarm (*alert fatigue*).

## Referensi

1. Grafana Labs. *Grafana Documentation — Dashboard Best Practices & Alerting Engine Architecture*. https://grafana.com/docs/
2. Prometheus Authors. *Alerting based on Metrics: The Firing & Pending State Machine*. https://prometheus.io/docs/alerting/latest/overview/
3. Endsley, M. R. *Designing for Situation Awareness: An Approach to User-Centered Design*. CRC Press.
