# Modul E05 — Geospatial Telemetry, Geofencing & Spatial Aggregation (H3 / S2)

## Tujuan pembelajaran
Setelah menyelesaikan modul ini, peserta didik mampu:
1. Mengimplementasikan formula Haversine untuk menghitung jarak geodesik antar-aset kota pada elipsoid WGS84.
2. Merancang algoritma Ray-Casting Point-in-Polygon (PiP) berlatensi sub-milidetik untuk deteksi pelanggaran batas geofence.
3. Menerapkan sistem indeksasi grid heksagonal diskret (Uber H3 Resolution 8) untuk masking privasi spasial warga.
4. Mengintegrasikan telemetri armada dinas ke dalam pipeline analitik spasial perkotaan.

## Prasyarat
- Bab Kurikulum Inti Prasyarat: Chapter 11, Chapter 21, Chapter 25.
- Modul Jalur Peminatan Prasyarat: Modul E01.
- Pemrograman Python 3.x dan pemahaman dasar aljabar linier serta kalkulus diskrit.

## Konsep dan teori

### 1. Peran Data Geospasial dalam Sistem Kota Cerdas
Setiap data telemetri perkotaan (posisi armada bus TransJakarta, sensor ketinggian genangan air di jalan protokol, kebisingan konstruksi) memiliki komponen spasial WGS84 (*latitude*, *longitude*, *altitude*). Tanpa pengolahan spasial yang efisien, data hanya berupa angka tanpa konteks geografis.

### 2. Geodesi Komputasi: Jarak Haversine vs Euclidean
Bumi bukanlah bidang datar melainkan elipsoid. Menghitung jarak menggunakan formula Pythagoras Euclidean ($d = \sqrt{\Delta x^2 + \Delta y^2}$) pada koordinat derajat akan menghasilkan distorsi kesalahan hingga puluhan persen karena konvergensi garis bujur. Formula **Haversine** menghitung jarak lingkaran besar (*great-circle distance*) pada permukaan bola dengan mempertimbangkan kelengkungan bumi secara akurat.

### 3. Geofencing: Algoritma Ray-Casting Point-in-Polygon (PiP)
Geofence adalah batas geografis virtual yang didefinisikan sebagai poligon arbitrer (misalnya zona evakuasi bencana banjir DKI Jakarta atau area steril istana negara).
Untuk menentukan secara real-time apakah suatu kendaraan atau sensor berada di dalam batas geofence, algoritma **Ray-Casting (Jordan Curve Theorem)** memproyeksikan sinar horizontal imajiner dari titik uji ke arah tak hingga:
- Jika sinar memotong sisi poligon dalam jumlah **ganjil**, titik berada di **dalam** poligon.
- Jika sinar memotong sisi poligon dalam jumlah **genap**, titik berada di **luar** poligon.
Algoritma ini memiliki kompleksitas linear $O(V)$ di mana $V$ adalah jumlah simpul sudut poligon, memungkinkannya dieksekusi dalam sub-milidetik.

### 4. Agregasi Grid Heksagonal Uber H3 & Perlindungan Privasi
Mempublikasikan koordinat GPS presisi mentah ($10^{-5}$ derajat $\approx 1\text{ meter}$) ke portal publik kota cerdas melanggar privasi warga (dapat melacak rute perjalanan pribadi pengemudi armada sewaan).
Sistem grid diskret global **Uber H3** membagi permukaan bumi ke dalam sel-sel heksagonal seragam:
- Sel heksagonal dipilih karena memiliki jarak tetangga konstan (*constant neighbor distance*) dan artefak kuantisasi tepi yang jauh lebih rendah dibanding grid persegi.
- Pada **Resolusi 8**, luas sel sekitar $0{,}73\text{ km}^2$ (panjang tepi $\approx 460\text{ meter}$).
- Koordinat mentah dipetakan ke dalam identifier H3 ("h3_index"), memungkinkan agregasi kepadatan trafik perkotaan (*heatmaps*) tanpa mengekspos jejak individual.

### 5. Formulasi Matematis Geodesi & Deteksi Geofence

1. **Formula Haversine Jarak Geodesik WGS84**:
   $$
   \Delta \phi = \phi_2 - \phi_1, \quad \Delta \lambda = \lambda_2 - \lambda_1
   $$
   $$
   a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1) \cos(\phi_2) \sin^2\left(\frac{\Delta \lambda}{2}\right)
   $$
   $$
   c = 2 \cdot \operatorname{atan2}\left(\sqrt{a}, \sqrt{1-a}\right) \implies d = R_{\text{earth}} \cdot c
   $$
   dengan $R_{\text{earth}} = 6371000\text{ meter}$.

2. **Perpotongan Garis Sinar Ray-Casting**:
   Persamaan titik potong sinar $y = y_0$ dengan segmen garis poligon antara $(x_1, y_1)$ dan $(x_2, y_2)$:
   $$
   x_{\text{intersect}} = x_1 + \frac{y_0 - y_1}{y_2 - y_1} (x_2 - x_1)
   $$
   Sinar memotong segmen jika $y_0 \in (\min(y_1, y_2), \max(y_1, y_2)]$ dan $x_0 \le x_{\text{intersect}}$.

## Latihan

## Latihan Pemahaman Mandiri

1. **Keunggulan Grid Heksagonal H3**:
   - *Soal*: Mengapa arsitektur kota cerdas modern lebih memilih grid heksagonal (seperti Uber H3) dibandingkan grid bujursangkar (seperti sistem ubin peta konvensional) untuk pemodelan dispersi polusi udara?
   - *Jawaban*: Grid heksagonal memiliki sifat bahwa setiap sel memiliki 6 tetangga yang berjarak identik sama dari pusat ($d_i = \text{konstan}$). Pada grid persegi, tetangga diagonal memiliki jarak $\sqrt{2} \times$ lebih jauh dibanding tetangga ortogonal. Sifat isotropik seragam heksagon ini mencegah bias arah saat mensimulasikan penyebaran zat pencemar udara perkotaan.

2. **Dampak Kompleksitas Poligon Geofence**:
   - *Soal*: Jika suatu dinas perkotaan mendefinisikan geofence batas kecamatan dengan 10.000 titik sudut poligon, apa dampak komputasinya jika ada 50.000 armada kendaraan yang mengirim GPS tiap detik? Bagaimana optimasi arsitekturalnya?
   - *Jawaban*: Pengecekan Ray-Casting $O(V)$ secara naif akan memerlukan $50000 \times 10000 = 500\text{ juta}$ operasi potong garis per detik, membebani CPU server. Solusi optimasi: Terapkan penapisan tahap awal menggunakan *Bounding Box (BBox)* atau pemetaan sel H3 level kasar. Titik yang berada di luar kotak pembatas BBox langsung diabaikan dalam waktu $O(1)$, sehingga uji Ray-Casting poligon penuh hanya dijalankan untuk titik-titik yang lolos penapisan kasar.

## Tugas

## Penugasan Mandiri: Pemodelan Geofence Multi-Zona & Indeksasi H3

1. Buat script yang mendefinisikan tiga tingkatan zona bahaya banjir (Zona Bahaya Merah, Zona Waspada Kuning, Zona Aman Hijau).
2. Lakukan evaluasi ray-casting terhadap 1.000 titik sampel koordinat acak di wilayah perkotaan.
3. Hitung persentase simpul yang berada di masing-masing zona banjir.
4. Lakukan agregasi kepadatan sensor per sel H3 dan visualisasikan peta panas (heatmap) konsentrasi aset kota.

## Ringkasan
- Modul E05 memberikan pemahaman mendalam dan terapan mengenai Geospatial Telemetry, Geofencing & Spatial Aggregation (H3 / S2) pada tingkat kedalaman L2: Undergraduate Complete.
- Seluruh algoritma komputasi dan pemodelan matematis telah divalidasi melalui eksekusi simulasi mandiri [geospatial_telemetry_h3_sim.py](src/geospatial_telemetry_h3_sim.py) yang dapat direproduksi 100%.
- Kepatuhan standar internasional dan batas keselamatan operasional menjadi pilar utama dalam perancangan arsitektur rekayasa ini.

## Referensi
1. Uber H3: A Hexagonal Hierarchical Spatial Index, [https://h3geo.org/docs/](https://h3geo.org/docs/) (diperiksa 2026-11-18).
2. Sinnott, R. W. - Virtues of the Haversine, Sky and Telescope, vol. 68, [https://en.wikipedia.org/wiki/Haversine_formula](https://en.wikipedia.org/wiki/Haversine_formula) (diperiksa 2026-11-18).
