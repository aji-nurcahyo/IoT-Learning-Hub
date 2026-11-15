# Tugas Mandiri: Rancang Bangun Engine Time-Series & Downsampling Rollup

## Deskripsi Tugas

Tugas ini melatih mahasiswa menguasai arsitektur penyimpanan basis data deret waktu (*time-series storage*), teknik partisi indeks temporal, perancangan agregasi berjenjang (*continuous rollups*), serta penegakan kebijakan retensi data (*retention aging policy*) pada platform IoT terdistribusi.

## Petunjuk Pengerjaan

1. **Desain Skema & Indeks Komposit**:
   - Susun struktur tabel `telemetry_raw` yang menampung kolom `device_id`, `timestamp`, `temp_c`, `humidity_pct`, dan `battery_mv`.
   - Buat indeks B-Tree gabungan pada pasangan kolom `(device_id, timestamp)`.
2. **Bulk Ingestion Pipeline**:
   - Bangun metode penambahan data massal `insert_raw_batch` yang memanfaatkan transaksi atomik untuk memaksimalkan throughput penulisan disk.
3. **Mesin Agregasi Downsampling (Rollup Engine)**:
   - Buat tabel `telemetry_rollup_1m` dengan kunci primer gabungan `(device_id, window_start)`.
   - Tuliskan kueri agregasi SQL yang mengelompokkan data mentah ke dalam ember 60 detik dan menghitung metrik `avg_temp`, `min_temp`, `max_temp`, dan `sample_count`.
4. **Pembersihan Retensi Otomatis**:
   - Terapkan fungsi pembersihan data lama `apply_retention_policy` berdasarkan ambang batas waktu putus (*cutoff timestamp*).
   - Pastikan data ringkasan di tabel rollup tetap terjaga utuh meskipun data mentahnya telah terhapus.
5. **Kalkulator Estimasi Kapasitas Penyimpanan**:
   - Implementasikan fungsi matematis `estimate_storage_requirements` untuk menghitung proyeksi konsumsi kapasitas disk armada sensor multi-perangkat.

## Rubrik Penilaian (Total 100 Poin)

| No | Kriteria Evaluasi | Bobot | Deskripsi Capaian |
| :---: | :--- | :---: | :--- |
| 1 | **Skema Time-Series & Desain Indeks** | 35 | Tabel data mentah dan tabel rollup dirancang optimal; indeks komposit temporal dikonfigurasi tepat untuk kueri cepat. |
| 2 | **Akurasi Downsampling & Rollup Pipeline** | 35 | Logika pembagian ember waktu 60 detik benar; metrik agregat statistik (avg, min, max, count) terhitung akurat dan konsisten. |
| 3 | **Penegakan Retensi & Model Estimasi Kapasitas** | 30 | Pembersihan retensi menghapus data mentah lawas tanpa mengorbankan tabel rollup; model matematis kalkulasi disk akurat. |
