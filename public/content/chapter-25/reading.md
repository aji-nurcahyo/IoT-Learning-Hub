# Chapter 25 — Time-Series Storage & Data Retention

Arsitektur penyimpanan basis data relasional tradisional (OLTP) dirancang untuk transaksi perbankan atau e-commerce yang melibatkan pembacaan acak, pembaruan (*in-place updates*), dan integritas referensial antar tabel (*foreign keys*). Karakteristik data IoT sangat bertolak belakang: aliran data deret waktu (*time-series data*) bersifat murni penambahan (*append-only writes*), memiliki volume yang masif, dan kueri selalu dibatasi oleh rentang waktu tertentu (`WHERE timestamp BETWEEN t1 AND t2`).

Menyimpan miliaran baris data mentah frekuensi tinggi selamanya di kartu memori Raspberry Pi atau cloud tanpa strategi penataan akan berujung pada kehabisan kapasitas disk, degradasi kecepatan kueri, dan biaya operasional yang tidak terkendali. Bab ini membahas arsitektur penyimpanan deret waktu, indeks komposit temporal, agregasi berjenjang (*continuous downsampling rollups*), kebijakan pembersihan data usang (*data retention policies*), serta pemodelan matematis estimasi kebutuhan kapasitas penyimpanan.

![Siklus Hidup Data Time-Series: Ingestion, Downsampling, Retensi, dan Kueri Analitik](content/chapter-25/diagram.svg)

## Tujuan pembelajaran

Setelah menyelesaikan bab ini, Anda diharapkan mampu:

1. **Memahami Karakteristik Beban Kerja Time-Series**: Membedakan pola akses data deret waktu (tulis sekuensial, kueri rentang waktu, agregasi) dari basis data transaksional umum.
2. **Merancang Skema Basis Data Terindeks**: Mengonfigurasi tabel penyimpanan deret waktu dengan pemisahan tag dimensi (*device_id*) dan field metrik (*temp*, *humidity*), serta indeks B-Tree gabungan `(device_id, timestamp)`.
3. **Membangun Pipeline Downsampling (Rollup Engine)**: Menerapkan mekanisme agregasi otomatis yang mengonversi data resolusi tinggi ($1\text{–}5\text{ detik}$) menjadi ringkasan berkala ($1\text{ menit}$, $1\text{ jam}$) menggunakan metrik statistik (`avg`, `min`, `max`, `count`).
4. **Menerapkan Kebijakan Retensi Data (Retention Policies)**: Membangun logika pembersihan otomatis (*aging purge*) untuk membuang data mentah lama secara berkala tanpa merusak data tren jangka panjang.
5. **Menghitung Estimasi Kebutuhan Kapasitas Disk**: Menerapkan formula kalkulasi kebutuhan penyimpanan berdasarkan ukuran rekaman, frekuensi sampling, jumlah simpul sensor, dan durasi retensi.

## Prasyarat

- Memahami konsep basis data SQL dasar (DDL, DML, `SELECT`, `WHERE`, `GROUP BY`).
- Memahami konsep data model dan stempel waktu UTC dari [Chapter 21](chapter-21).
- Memahami sistem berkas Linux dan I/O disk dari [Chapter 22](chapter-22).

## Konsep dan teori

### 1. Perbedaan Mendasar Time-Series vs Transaksional

| Parameter | Basis Data Transaksional (OLTP) | Basis Data Deret Waktu (Time-Series) |
| :--- | :--- | :--- |
| **Operasi Dominan** | Baca dan Perbarui Acak (*Random Update*) | Penambahan Beruntun (*Append-Only*) |
| **Pola Kueri** | Berdasarkan ID primer tunggal (`WHERE id = 42`) | Rentang Waktu Komposit (`WHERE dev='A' AND ts BETWEEN t1 AND t2`) |
| **Volume Data** | Megabyte hingga Gigabyte moderat | Gigabyte hingga Terabyte masif |
| **Pembaruan Data** | Sangat sering dimodifikasi (*state change*) | Data yang telah tercatat tidak pernah diubah (*immutable*) |
| **Siklus Hidup** | Bertahan selamanya hingga dihapus pengguna | Memiliki masa berlaku (*aging/retention schedule*) |

### 2. Desain Skema & Indeks Komposit

Sebuah rekaman telemetri deret waktu terdiri atas tiga komponen inti:
1. **Timestamp**: Waktu pengambilan data (Unix Epoch UTC dalam integer).
2. **Tags (Dimensi)**: Metadata dengan kardinalitas relatif rendah untuk pengelompokan (seperti `device_id`, `site`, `rack`).
3. **Fields (Metrik)**: Nilai pengukuran kontinu numerik (seperti `temp_c`, `humidity_pct`, `battery_mv`).

Untuk mempercepat kueri analitik, indeks komposit B-Tree dibentuk pada kombinasi `(device_id, timestamp)`. Dengan indeks ini, pencarian data $1\text{ hari}$ untuk satu perangkat di antara jutaan rekaman hanya membutuhkan penelusuran pohon berkecepatan $O(\log N)$ alih-alih pemindaian seluruh tabel (*Full Table Scan*).

### 3. Pipeline Downsampling & Rollup Berjenjang

Menampilkan grafik $1\text{ tahun}$ di dashboard pemantauan tidak membutuhkan data frekuensi $5\text{ detik}$ ($6{,}3\text{ juta}$ titik data). Layar monitor hanya memiliki resolusi $\sim 1920\text{ piksel}$, sehingga memuat jutaan data titik hanya membebani memori browser dan CPU server.

**Downsampling** merangkum data frekuensi tinggi ke dalam ember waktu (*time buckets*):

$$\text{Bucket Start} = \left\lfloor \frac{\text{timestamp}}{\Delta T} \right\rfloor \times \Delta T$$

Untuk setiap bucket $\Delta T$ (misal $60\text{ detik}$):
- `sample_count` = $\sum 1$
- `avg_temp` = $\frac{1}{N} \sum T_i$
- `min_temp` = $\min(T_i)$
- `max_temp` = $\max(T_i)$

### 4. Kebijakan Retensi Data (Retention Policy)

Strategi pengelolaan data berjenjang (*Multi-Tier Data Lifecycle*):
1. **Tier 1 (Raw Stream)**: Resolusi $5\text{ detik}$. Disimpan selama **7 hari** untuk keperluan diagnostik dan troubleshooting mendalam.
2. **Tier 2 (1-Minute Rollup)**: Resolusi $1\text{ menit}$. Disimpan selama **30–90 hari** untuk analisis performa operasional bulanan.
3. **Tier 3 (1-Hour Rollup)**: Resolusi $1\text{ jam}$. Disimpan selama **1–5 tahun** untuk laporan tahunan dan analisis tren musiman.

Pembersihan data mentah dilakukan dengan kueri terjadwal:
```sql
DELETE FROM telemetry_raw WHERE timestamp < (? - 7 * 86400);
```

### 5. Formula Matematis Estimasi Kapasitas Penyimpanan

Kebutuhan kapasitas penyimpanan mentah ($S_{\text{raw}}$) dan agregat ($S_{\text{rollup}}$) dihitung menggunakan persamaan:

$$S_{\text{raw}} = N_{\text{dev}} \times \left( \frac{86400}{\Delta t_{\text{sample}}} \right) \times D_{\text{retention}} \times B_{\text{row}}$$

Sebagai contoh:
- $N_{\text{dev}} = 100\text{ simpul sensor}$
- $\Delta t_{\text{sample}} = 5\text{ detik}$ ($17.280\text{ sampel/hari/simpul}$)
- $D_{\text{retention}} = 7\text{ hari}$
- $B_{\text{row}} = 40\text{ byte/rekaman}$ (SQLite overhead & index)

Maka total baris mentah:
$$\text{Total Baris} = 100 \times 17.280 \times 7 = 12.096.000\text{ baris}$$
$$\text{Total Kapasitas Mentah} \approx 483{,}84\text{ MB}$$

Dengan menerapkan downsampling 1-menit untuk retensi 365 hari, total ruang disk yang dibutuhkan seluruh armada selama satu tahun penuh hanya berkisar $\sim 2{,}8\text{ GB}$, sangat aman ditampung di kartu micro-SD $16\text{ GB}$ atau $32\text{ GB}$ Raspberry Pi.

## Latihan

1. **Perbandingan Struktur Indeks**:
   Jelaskan mengapa membuat indeks hanya pada kolom `timestamp` kurang efisien jika sistem Anda memantau 500 perangkat berbeda, dibandingkan menggunakan indeks gabungan `(device_id, timestamp)`.
2. **Perhitungan Storage Downsampling**:
   Sebuah armada IoT memiliki 50 perangkat dengan frekuensi sampling 10 detik ($B_{\text{row}} = 35\text{ byte}$).
   - Hitung total ruang penyimpanan yang dibutuhkan jika data mentah disimpan selama 30 hari.
   - Jika data tersebut langsung diringkas ke rollup 5 menit ($B_{\text{rollup}} = 45\text{ byte}$), hitung ukuran penyimpanan untuk 30 hari dan persentase penghematan ruang disk.
3. **Dampak Perintah DELETE Massal**:
   Pada basis data SQLite di kartu flash micro-SD, mengeksekusi `DELETE FROM telemetry_raw WHERE timestamp < X` menghapus baris data tetapi tidak langsung memperkecil ukuran file basis data di disk (*fragmented free pages*). Perintah SQLite apa yang harus dijalankan untuk merebut kembali ruang kosong tersebut (*reclaim space*), dan mengapa eksekusi perintah tersebut tidak boleh dilakukan terlalu sering?

## Tugas

Rancang dan implementasikan mesin penyimpanan deret waktu berbasis SQLite menggunakan Python:

1. **Inisialisasi Skema & Indeks Komposit**:
   Susun skema tabel `telemetry_raw` dan `telemetry_rollup_1m` lengkap dengan indeks komposit `(device_id, timestamp)`.
2. **Fungsi Bulk Ingestion**:
   Terapkan metode `insert_raw_batch` yang memasukkan puluhan baris data dalam satu transaksi tunggal untuk mengoptimalkan kecepatan tulis disk.
3. **Pipeline Downsampling Otomatis**:
   Implementasikan fungsi `execute_downsampling_1m` yang merangkum data mentah ke dalam ember 60 detik dan menghitung metrik agregat (`count`, `avg`, `min`, `max`).
4. **Kebijakan Pembersihan Retensi**:
   Terapkan fungsi `apply_retention_policy` yang membuang data mentah yang melampaui batas retensi, serta buktikan bahwa data ringkasan di tabel rollup tetap aman dan utuh.
5. **Kalkulator Estimasi Kapasitas**:
   Bangun fungsi `estimate_storage_requirements` dan hitung kebutuhan disk armada 100 perangkat untuk retensi mentah 7 hari dan rollup 365 hari.

### Rubrik Penilaian

| Kriteria | Bobot | Deskripsi Capaian |
| :--- | :---: | :--- |
| **Desain Skema & Efisiensi Indeks** | 35% | Struktur tabel dan indeks komposit tersusun benar; bulk insert dieksekusi dalam transaksi atomik yang efisien. |
| **Pipeline Downsampling & Agregasi** | 35% | Perhitungan bucket waktu 60 detik dan kalkulasi metrik agregat (avg/min/max/count) terbukti tepat dan konsisten. |
| **Kebijakan Retensi & Model Estimasi** | 30% | Data lama terhapus sesuai batas retensi tanpa merusak tabel agregasi; fungsi estimasi kapasitas disk menghasilkan kalkulasi akurat. |

## Ringkasan

1. **Karakteristik Time-Series**: Sifat data yang murni append-only dan berbasis interval waktu menuntut skema penyimpanan khusus dengan indeks komposit temporal.
2. **Keuntungan Downsampling**: Mengonversi rekaman frekuensi tinggi menjadi rollup berkala memangkas ukuran basis data hingga $>90\%$ tanpa menghilangkan wawasan historis.
3. **Penyimpanan Berjenjang**: Menerapkan retensi bertingkat (mentah 7 hari, 1 menit 90 hari, 1 jam tahunan) menjaga performa sistem tetap prima dalam jangka panjang.
4. **Estimasi Terukur**: Perhitungan kapasitas penyimpanan disk matematis memastikan sistem tidak mengalami kegagalan crash akibat kehabisan memori.

## Referensi

1. SQLite Consortium. *Query Planning and Indexing in SQLite*. https://www.sqlite.org/queryplanner.html
2. InfluxData. *Time-series Database Engine Architecture and Downsampling Best Practices*. InfluxDB Documentation.
3. Kleppmann, M. *Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*. O'Reilly Media. Chapter: Storage and Retrieval.
