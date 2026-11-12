# Tugas & Rubrik — Chapter 08

## Skenario Tugas: Validasi Kalibrasi & Laporan Ketidakpastian Sensor

Anda diberikan dataset perbandingan sensor terhadap instrumen referensi (gunakan `telemetry.csv` atau kumpulkan dataset simulasi/pengukuran berlabel sumber jelas dengan minimal 5 titik rentang ukur dan 5 pengulangan pada titik tengah). Susun laporan validasi metrologi sensor beserta implementasi akuisisi terkalibrasi pada *Firmware* `ESP32-DevKitC V4`.

## Deliverables

1. **Prosedur Kalibrasi & Stabilitas**: Jelaskan titik acuan, durasi stabilisasi ($\ge 5\tau$), dan cara menghindari *self-heating*.
2. **Perhitungan Model & Validasi**: Hitung parameter *two-point* dan *least-squares*, tampilkan perbandingan RMSE sebelum vs sesudah kalibrasi.
3. **Budget Ketidakpastian**: Hitung $u_A$, $u_B$ (referensi + resolusi), $u_c$, dan $U$ ($k=2$) lengkap dengan satuan.
4. **Firmware / Skrip Akuisisi**: Sertakan implementasi kalibrasi, *averaging*, dan deteksi *fault* sensor (`open/short`), serta nyatakan status verifikasi secara jujur.

## Rubrik Penilaian (Total 100 Poin)

| Kriteria | Bobot | Deskripsi Penilaian |
| --- | --- | --- |
| **Metodologi kalibrasi & penanganan waktu respons** | **25** | Titik acuan valid, syarat stabilitas $5\tau$ diperhatikan, serta *systematic* vs *random error* teridentifikasi tepat. |
| **Perhitungan model kalibrasi & validasi error** | **30** | Rumus *slope/offset* tepat dan perbandingan RMSE sebelum vs sesudah kalibrasi dihitung akurat. |
| **Analisis ketidakpastian (Type A, Type B & k=2)** | **25** | Perhitungan $u_A$, $u_B$, $u_c$, dan pelaporan akhir ($\bar{x} \pm U$) konsisten dengan kaidah metrologi. |
| **Implementasi akuisisi & kejujuran data** | **20** | Kode akuisisi menyertakan *averaging* & deteksi *fault*; sumber data (sintetis vs fisik) dilabeli jujur. |

