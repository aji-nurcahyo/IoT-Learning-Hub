# Panduan Implementasi Kode — Chapter 25

Dokumentasi ini menjelaskan arsitektur skrip [`timeseries_retention_engine.py`](content/chapter-25/src/timeseries_retention_engine.py).

## Struktur Program

1. **Kelas `TimeSeriesEngine`**:
   - `_init_schema`: Mendefinisikan tabel `telemetry_raw` (resolusi tinggi) dan `telemetry_rollup_1m` (resolusi agregat) lengkap dengan indeks komposit `idx_raw_dev_ts` pada kolom `(device_id, timestamp)`.
   - `insert_raw_batch`: Memasukkan puluhan rekaman dalam satu transaksi commit `executemany` tunggal untuk efisiensi I/O.
   - `execute_downsampling_1m`: Menggunakan kueri SQL cerdas dengan pengelompokan `(timestamp / 60) * 60` untuk membagi data ke dalam jendela waktu 1 menit tanpa tumpang tindih. Menghitung `AVG`, `MIN`, `MAX`, dan `COUNT(*)`.
   - `apply_retention_policy`: Mengeksekusi `DELETE FROM telemetry_raw WHERE timestamp < ?` untuk membuang data yang lebih tua dari batas usia retensi.
   - `query_range` & `query_rollups`: Menyediakan antarmuka kueri deret waktu cepat yang memanfaatkan indeks komposit.
2. **Fungsi `estimate_storage_requirements`**:
   - Menghitung jumlah baris data mentah per hari: $N_{\text{dev}} \times (86400 / \Delta t)$.
   - Mengalikan dengan durasi retensi dan estimasi byte per baris basis data.
   - Menghitung total kebutuhan disk mentah ditambah rollup tahunan dalam satuan Megabyte dan Gigabyte.

## Eksekusi Pengujian

Jalankan pengujian engine dan kalkulasi kapasitas langsung dari terminal:

```bash
python public/content/chapter-25/src/timeseries_retention_engine.py
```
