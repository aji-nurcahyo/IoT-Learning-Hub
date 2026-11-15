# Bukti Pengujian & Hasil Eksekusi — Chapter 25

Pengujian mesin penyimpanan deret waktu SQLite, pipeline downsampling rollup, dan kebijakan retensi data dieksekusi menggunakan lingkungan runtime Python 3.

## Perintah Eksekusi

```bash
python public/content/chapter-25/src/timeseries_retention_engine.py
```

## Hasil Keluaran Terminal (Standard Output)

```text
=== Time-Series Storage & Retention Verification Suite ===
Test 1 - Bulk Ingestion: Berhasil memasukkan 30 baris data mentah.

Test 2 - Downsampling Rollup (1-Menit):
   Jumlah jendela agregasi terbuat: 2
   Jendela 1762822800: Count=15, AvgTemp=26.7 C (Min=26.0, Max=27.4)
   Jendela 1762822860: Count=15, AvgTemp=28.7 C (Min=28.0, Max=29.4)

Test 3 - Retention Policy Purge:
   Data mentah terhapus (> 60s): 18 baris
   Sisa data mentah aktif       : 12 baris
   Data rollup agregasi tetap utuh: 2 jendela (Data historis terlindungi).

Test 4 - Storage Capacity Estimation:
   100 Perangkat @ 5s sampling:
   - Raw Storage (7 hari)    : 12096000 baris | 461.43 MB
   - Rollup Storage (365 hari): 52560000 baris | 2406.01 MB
   - Total Kebutuhan Disk    : 2.8 GB

Semua pengujian time-series storage & retensi berhasil diselesaikan.
```

## Analisis Hasil

1. **Efisiensi Ingestion & Pengelompokan**: Tiga puluh rekaman telemetri mentah yang terbagi dalam dua menit berbeda berhasil dikelompokkan ke dalam tepat dua jendela rollup 1 menit (`1762822800` dan `1762822860`) dengan masing-masing 15 sampel.
2. **Keandalan Agregasi**: Nilai rata-rata, batas minimum, dan batas maksimum suhu terhitung dengan presisi desimal yang akurat pada masing-masing jendela agregasi.
3. **Penegakan Retensi**: Pembersihan data mentah lawas berhasil membuang 18 baris yang melampaui batas retensi 60 detik tanpa menghapus data ringkasan di tabel rollup, membuktikan perlindungan kontinuitas data historis jangka panjang.
4. **Validasi Model Kapasitas**: Kalkulasi matematis membuktikan bahwa armada 100 perangkat dengan sampling 5 detik hanya membutuhkan ruang disk sebesar $\sim 2{,}8\text{ GB}$ untuk menyimpan data mentah 7 hari dan rollup 365 hari.
