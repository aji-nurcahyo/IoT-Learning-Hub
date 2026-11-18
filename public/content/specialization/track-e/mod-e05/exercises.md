# Latihan Terstruktur: Modul E05

## Latihan Pemahaman Mandiri

1. **Keunggulan Grid Heksagonal H3**:
   - *Soal*: Mengapa arsitektur kota cerdas modern lebih memilih grid heksagonal (seperti Uber H3) dibandingkan grid bujursangkar (seperti sistem ubin peta konvensional) untuk pemodelan dispersi polusi udara?
   - *Jawaban*: Grid heksagonal memiliki sifat bahwa setiap sel memiliki 6 tetangga yang berjarak identik sama dari pusat ($d_i = \text{konstan}$). Pada grid persegi, tetangga diagonal memiliki jarak $\sqrt{2} \times$ lebih jauh dibanding tetangga ortogonal. Sifat isotropik seragam heksagon ini mencegah bias arah saat mensimulasikan penyebaran zat pencemar udara perkotaan.

2. **Dampak Kompleksitas Poligon Geofence**:
   - *Soal*: Jika suatu dinas perkotaan mendefinisikan geofence batas kecamatan dengan 10.000 titik sudut poligon, apa dampak komputasinya jika ada 50.000 armada kendaraan yang mengirim GPS tiap detik? Bagaimana optimasi arsitekturalnya?
   - *Jawaban*: Pengecekan Ray-Casting $O(V)$ secara naif akan memerlukan $50000 \times 10000 = 500\text{ juta}$ operasi potong garis per detik, membebani CPU server. Solusi optimasi: Terapkan penapisan tahap awal menggunakan *Bounding Box (BBox)* atau pemetaan sel H3 level kasar. Titik yang berada di luar kotak pembatas BBox langsung diabaikan dalam waktu $O(1)$, sehingga uji Ray-Casting poligon penuh hanya dijalankan untuk titik-titik yang lolos penapisan kasar.
