# Latihan Soal & Praktik — Chapter 25

## Bagian A — Soal Konseptual

1. **Perbandingan Skema Relasional vs Time-Series**:
   Jelaskan mengapa menggunakan tabel normalisasi ganda dengan banyak relasi `FOREIGN KEY` (seperti memisahkan tabel `Sensor`, `Location`, `Reading`, dan `Calibration`) dapat memperlambat performa penulisan telemetri massal pada sistem IoT frekuensi tinggi.
2. **Keunggulan Indeks Komposit**:
   Diberikan kueri SQL berikut:
   ```sql
   SELECT timestamp, temp_c 
   FROM telemetry_raw 
   WHERE device_id = 'node-alpha' 
     AND timestamp BETWEEN 1762822800 AND 1762826400;
   ```
   Jelaskan bagaimana indeks komposit `(device_id, timestamp)` membantu mesin basis data mengeksekusi kueri tersebut secara efisien tanpa harus memeriksa seluruh baris milik perangkat lain.
3. **Penyimpanan Nilai Ekstrem pada Downsampling**:
   Mengapa dalam proses agregasi *downsampling*, selain menyimpan nilai rata-rata (`avg`), sistem pemantauan industri wajib menyimpan metrik `min` dan `max` dari setiap jendela waktu? Berikan contoh kasus kegagalan mesin yang dapat terlewatkan jika hanya nilai rata-rata yang disimpan.

## Bagian B — Soal Praktik Komputasi

1. **Kalkulasi Kebutuhan Penyimpanan Disk**:
   Sebuah gedung pintar memiliki $200$ sensor suhu dan kelembapan. Setiap sensor mengirimkan sampel data setiap $5\text{ detik}$.
   - a. Hitung berapa banyak baris data mentah yang dihasilkan oleh seluruh gedung dalam waktu $14\text{ hari}$ ($D_{\text{raw}} = 14$).
   - b. Jika satu baris data rata-rata menghabiskan $42\text{ byte}$ memori penyimpanan, hitung ukuran data mentah tersebut dalam megabyte (MB).
   - c. Jika data mentah diringkas menjadi agregat per menit ($1\text{ menit} = 60\text{ detik}$) untuk disimpan selama $365\text{ hari}$ dengan ukuran $50\text{ byte}$ per baris rollup, hitung ukuran data rollup tahunan tersebut dalam gigabyte (GB).
2. **Eksplorasi Skrip Time-Series Engine**:
   Jalankan skrip [`timeseries_retention_engine.py`](content/chapter-25/src/timeseries_retention_engine.py). Modifikasi fungsi `main()` untuk menambahkan sensor kedua bernama `node-beta` dengan 20 rekaman data. Jalankan kembali dan buktikan bahwa tabel rollup berhasil mengelompokkan data per menit untuk masing-masing perangkat secara terpisah.
