# Tugas Terbimbing: Pemodelan Digital Twin Sistem Termal & Simulasi What-If

## Deskripsi Tugas

Dalam tugas ini, Anda diminta membangun sistem simulasi kembaran digital (*Digital Twin*) untuk pemantauan dinamika termal perangkat keras IoT serta memvalidasi mekanisme sinkronisasi state fisik-digital dan evaluasi skenario prediktif (*What-If analysis*).

Tugas ini mewajibkan:
1. Pemodelan sistem termal 1-orde berbasis persamaan diferensial dinamika energi (Hukum Pendinginan Newton & Pemanasan Joule) dengan integrasi numerik Euler diskrit.
2. Implementasi modul *Digital Twin Synchronizer* yang menerima aliran telemetri suhu fisik, memperbarui estimasi model secara real-time, dan memantau galat residu (*residual discrepancy*) untuk mendeteksi deviasi operasional.
3. Eksekusi simulasi *What-If Analysis* yang memproyeksikan kenaikan suhu sistem di masa depan jika daya dinaikkan secara drastis, sebagai mekanisme verifikasi keselamatan sebelum perintah aktuasi fisik diterapkan.

## Petunjuk Pengumpulan

1. Kode sumber simulasi Python: `public/content/chapter-36/src/digital_twin_sim.py`.
2. Laporan analisis teknis yang mencakup tabel sinkronisasi langkah-demi-langkah, evaluasi galat residu, dan analisis kurva pemanasan skenario prediktif.

## Rubrik Penilaian (Total: 100 Poin)

| Kriteria | Bobot | Deskripsi |
|---|:---:|---|
| **Akurasi Model Matematika Dinamika Termal** | 35 Poin | Implementasi persamaan diferensial $C_{th}$ dan $R_{th}$ terbukti akurat, integrasi numerik Euler stabil, dan perhitungan suhu tunak sesuai kaidah termodinamika. |
| **Logika Sinkronisasi Fisik-Digital & Pemantauan Residu** | 35 Poin | Aliran data telemetri tersinkronisasi mulus, perhitungan selisih residu $|T_{fisik} - T_{digital}|$ terverifikasi otomatis, dan status penandaan deviasi berfungsi tepat. |
| **Kualitas Proyeksi Skenario Prediktif (What-If)** | 30 Poin | Simulasi prediktif memproyeksikan lintasan suhu masa depan secara realistis, menyajikan analisis batas keselamatan perangkat keras, dan memvalidasi keunggulan uji bebas risiko. |
